"""Step 5 — Book generation (runs after PRD is approved).

Generates each chapter individually:
  1. Selects the most relevant source chunks for the chapter.
  2. Calls the model with chapter spec + chunks.
  3. Logs every call.
"""
from app.ai import TextChunker, get_client, get_model_config
from app.ai.prompts import book as p
from app.services.log_service import AILogService
from app.services.pipeline.types import (
    BookSchema,
    ChapterSpecSchema,
    GeneratedChapterSchema,
    PRDSchema,
    PipelineContext,
)

_TOP_CHUNKS = 8        # max chunks injected per chapter call
_CHUNK_CHAR_LIMIT = 6_000  # truncate individual chunk if excessively long


def _build_requirements_list(chapter: ChapterSpecSchema) -> str:
    return "\n".join(f"  - {r}" for r in chapter.content_requirements)


def _build_source_text(ctx: PipelineContext, chapter: ChapterSpecSchema) -> str:
    keywords = chapter.key_sources + [chapter.title] + chapter.content_requirements[:3]
    relevant = TextChunker.select_relevant(ctx.chunks, keywords, top_n=_TOP_CHUNKS)
    parts = []
    for c in relevant:
        text = c.text[:_CHUNK_CHAR_LIMIT]
        parts.append(f"[Chunk {c.index + 1}]\n{text}")
    return "\n\n---\n\n".join(parts) or ctx.raw_text[:_CHUNK_CHAR_LIMIT]


async def _generate_chapter(
    ctx: PipelineContext,
    chapter: ChapterSpecSchema,
    prd: PRDSchema,
    client,
    config,
    log_svc: AILogService,
) -> GeneratedChapterSchema:
    source_chunks = _build_source_text(ctx, chapter)
    prompt = p.PROMPT.format(
        chapter_number=chapter.number,
        chapter_title=chapter.title,
        objective=chapter.objective,
        tone=prd.tone,
        audience=prd.target_audience,
        estimated_words=chapter.estimated_words,
        requirements_list=_build_requirements_list(chapter),
        source_chunks=source_chunks,
    )

    result, response = await client.complete_json(
        prompt=prompt,
        system=p.SYSTEM,
        schema_cls=GeneratedChapterSchema,
        model=config.model_id,
        max_tokens=config.max_tokens,
        temperature=0.3,
    )
    await log_svc.log(
        db=ctx.db, response=response, config=config,
        prompt=prompt, user_id=ctx.user_id, project_id=ctx.project_id,
        pipeline_step=f"book_generation/ch-{chapter.number}",
    )
    return result


async def run_book_generation(
    ctx: PipelineContext,
    prd: PRDSchema,
    log_svc: AILogService,
) -> BookSchema:
    client = get_client(ctx.model_alias)
    config = get_model_config(ctx.model_alias)

    chapters: list[GeneratedChapterSchema] = []
    for chapter_spec in prd.chapters:
        generated = await _generate_chapter(ctx, chapter_spec, prd, client, config, log_svc)
        chapters.append(generated)

    return BookSchema(title=prd.book_title, chapters=chapters)
