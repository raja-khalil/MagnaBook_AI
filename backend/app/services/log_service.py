from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.base_client import AIResponse
from app.ai.registry import ModelConfig, estimate_cost
from app.models.ai import AILog, APIProvider, APIUsage


class AILogService:
    """Writes AILog and APIUsage records to the database after each model call."""

    async def log(
        self,
        db: AsyncSession,
        response: AIResponse,
        config: ModelConfig,
        prompt: str,
        user_id: UUID | None = None,
        project_id: UUID | None = None,
        pipeline_step: str = "",
        status: str = "success",
        error_message: str | None = None,
    ) -> AILog:
        provider_id = await self._get_provider_id(db, response.provider)

        ai_log = AILog(
            user_id=user_id,
            project_id=project_id,
            provider_id=provider_id,
            model=response.model,
            prompt=f"[{pipeline_step}] {prompt}"[:10000],  # guard against huge prompts
            response=response.content[:20000] if response.content else None,
            tokens_input=response.tokens_input,
            tokens_output=response.tokens_output,
            latency_ms=response.latency_ms,
            status=status,
            error_message=error_message,
        )
        db.add(ai_log)

        cost = estimate_cost(config, response.tokens_input, response.tokens_output)
        usage = APIUsage(
            provider_id=provider_id,
            tokens_input=response.tokens_input,
            tokens_output=response.tokens_output,
            cost_usd=cost,
            endpoint=pipeline_step,
        )
        db.add(usage)

        await db.flush()
        return ai_log

    async def log_error(
        self,
        db: AsyncSession,
        config: ModelConfig,
        prompt: str,
        error: Exception,
        user_id: UUID | None = None,
        project_id: UUID | None = None,
        pipeline_step: str = "",
    ) -> None:
        provider_id = await self._get_provider_id(db, config.provider)
        ai_log = AILog(
            user_id=user_id,
            project_id=project_id,
            provider_id=provider_id,
            model=config.model_id,
            prompt=f"[{pipeline_step}] {prompt}"[:10000],
            response=None,
            tokens_input=0,
            tokens_output=0,
            latency_ms=None,
            status="error",
            error_message=str(error)[:2000],
        )
        db.add(ai_log)
        await db.flush()

    @staticmethod
    async def _get_provider_id(db: AsyncSession, provider_name: str) -> UUID | None:
        result = await db.execute(
            select(APIProvider.id).where(APIProvider.name == provider_name)
        )
        row = result.scalar_one_or_none()
        return row
