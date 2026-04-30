"""Step 2 — Editorial structuring.

Analyses parsed sections and produces theme, audience, genre, tone,
and a proposed chapter outline.
"""
from app.ai import get_client, get_model_config
from app.ai.prompts import structuring as p
from app.services.log_service import AILogService
from app.services.pipeline.types import ParsedDocumentSchema, PipelineContext, StructuredContentSchema


def _sections_to_text(parsed: ParsedDocumentSchema) -> str:
    lines: list[str] = []
    if parsed.title:
        lines.append(f"TITLE: {parsed.title}\n")
    for sec in parsed.sections:
        if sec.title:
            lines.append(f"## {sec.title}")
        lines.append(sec.content)
        lines.append("")
    return "\n".join(lines)


async def run_structuring(
    ctx: PipelineContext,
    parsed: ParsedDocumentSchema,
    log_svc: AILogService,
) -> StructuredContentSchema:
    client = get_client(ctx.model_alias)
    config = get_model_config(ctx.model_alias)

    sections_text = _sections_to_text(parsed)
    prompt = p.PROMPT.format(sections_text=sections_text)

    result, response = await client.complete_json(
        prompt=prompt,
        system=p.SYSTEM,
        schema_cls=StructuredContentSchema,
        model=config.model_id,
        max_tokens=4096,
        temperature=0.1,
    )
    await log_svc.log(
        db=ctx.db, response=response, config=config,
        prompt=prompt, user_id=ctx.user_id, project_id=ctx.project_id,
        pipeline_step="structuring",
    )
    return result
