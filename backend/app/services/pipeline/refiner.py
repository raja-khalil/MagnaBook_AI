"""Step 6 — Refinement.

Polishes each generated chapter for publication quality.
Preserves all factual content — only improves style, flow, and consistency.
"""
from app.ai import get_client, get_model_config
from app.ai.prompts import refinement as p
from app.services.log_service import AILogService
from app.services.pipeline.types import (
    BookSchema,
    GeneratedChapterSchema,
    PRDSchema,
    PipelineContext,
    RefinedBookSchema,
    RefinedChapterSchema,
)


async def _refine_chapter(
    ctx: PipelineContext,
    chapter: GeneratedChapterSchema,
    prd: PRDSchema,
    client,
    config,
    log_svc: AILogService,
) -> RefinedChapterSchema:
    prompt = p.PROMPT.format(
        book_title=prd.book_title,
        tone=prd.tone,
        audience=prd.target_audience,
        chapter_title=chapter.title,
        chapter_content=chapter.content,
    )

    result, response = await client.complete_json(
        prompt=prompt,
        system=p.SYSTEM,
        schema_cls=RefinedChapterSchema,
        model=config.model_id,
        max_tokens=config.max_tokens,
        temperature=0.2,
    )
    await log_svc.log(
        db=ctx.db, response=response, config=config,
        prompt=prompt, user_id=ctx.user_id, project_id=ctx.project_id,
        pipeline_step=f"refinement/ch-{chapter.title[:30]}",
    )
    return result


async def run_refinement(
    ctx: PipelineContext,
    book: BookSchema,
    prd: PRDSchema,
    log_svc: AILogService,
) -> RefinedBookSchema:
    client = get_client(ctx.model_alias)
    config = get_model_config(ctx.model_alias)

    refined_chapters: list[RefinedChapterSchema] = []
    for chapter in book.chapters:
        refined = await _refine_chapter(ctx, chapter, prd, client, config, log_svc)
        refined_chapters.append(refined)

    return RefinedBookSchema(title=book.title, chapters=refined_chapters)
