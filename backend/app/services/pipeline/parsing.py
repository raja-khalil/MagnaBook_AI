"""Step 1 — Document parsing.

Splits large documents into chunks, parses each, then merges sections.
For small documents a single call is made.
"""
from app.ai import TextChunker, get_client, get_model_config
from app.ai.prompts import parsing as p
from app.services.log_service import AILogService
from app.services.pipeline.types import ParsedDocumentSchema, ParsedSectionSchema, PipelineContext

_SINGLE_CALL_THRESHOLD = 12_000  # chars — below this, parse in one shot


async def run_parsing(ctx: PipelineContext, log_svc: AILogService) -> ParsedDocumentSchema:
    client = get_client(ctx.model_alias)
    config = get_model_config(ctx.model_alias)

    chunker = TextChunker()
    ctx.chunks = chunker.split(ctx.raw_text)

    if len(ctx.raw_text) <= _SINGLE_CALL_THRESHOLD:
        prompt = p.SINGLE_DOC.format(text=ctx.raw_text)
        result, response = await client.complete_json(
            prompt=prompt,
            system=p.SYSTEM,
            schema_cls=ParsedDocumentSchema,
            model=config.model_id,
            max_tokens=4096,
            temperature=0.0,
        )
        await log_svc.log(
            db=ctx.db, response=response, config=config,
            prompt=prompt, user_id=ctx.user_id, project_id=ctx.project_id,
            pipeline_step="parsing",
        )
        return result

    # Multi-chunk: map each chunk, then merge
    chunk_results: list[ParsedDocumentSchema] = []
    for chunk in ctx.chunks:
        prompt = p.CHUNK.format(text=chunk.text, index=chunk.index + 1, total=len(ctx.chunks))
        chunk_result, response = await client.complete_json(
            prompt=prompt,
            system=p.SYSTEM,
            schema_cls=ParsedDocumentSchema,
            model=config.model_id,
            max_tokens=4096,
            temperature=0.0,
        )
        await log_svc.log(
            db=ctx.db, response=response, config=config,
            prompt=prompt, user_id=ctx.user_id, project_id=ctx.project_id,
            pipeline_step=f"parsing/chunk-{chunk.index}",
        )
        chunk_results.append(chunk_result)

    return _merge_chunks(chunk_results)


def _merge_chunks(results: list[ParsedDocumentSchema]) -> ParsedDocumentSchema:
    title = next((r.title for r in results if r.title), None)
    sections: list[ParsedSectionSchema] = []
    for r in results:
        sections.extend(r.sections)
    return ParsedDocumentSchema(title=title, sections=sections)
