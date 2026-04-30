"""Step 3 — PRD generation.

Converts the editorial structure into a detailed book Product Requirements Document.
The PRD is the artifact submitted for human approval before book generation starts.
"""
import json

from app.ai import get_client, get_model_config
from app.ai.prompts import prd as p
from app.services.log_service import AILogService
from app.services.pipeline.types import PRDSchema, PipelineContext, StructuredContentSchema


async def run_prd_generation(
    ctx: PipelineContext,
    structured: StructuredContentSchema,
    log_svc: AILogService,
) -> PRDSchema:
    client = get_client(ctx.model_alias)
    config = get_model_config(ctx.model_alias)

    structured_text = json.dumps(structured.model_dump(), ensure_ascii=False, indent=2)
    prompt = p.PROMPT.format(structured_text=structured_text)

    result, response = await client.complete_json(
        prompt=prompt,
        system=p.SYSTEM,
        schema_cls=PRDSchema,
        model=config.model_id,
        max_tokens=6000,
        temperature=0.1,
    )
    await log_svc.log(
        db=ctx.db, response=response, config=config,
        prompt=prompt, user_id=ctx.user_id, project_id=ctx.project_id,
        pipeline_step="prd_generation",
    )
    return result
