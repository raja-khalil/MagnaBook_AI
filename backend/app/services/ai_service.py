"""AI Service — pipeline orchestrator.

Exposes two public phases:
  - phase_a: parse → structure → PRD  (returns PRD for human approval)
  - phase_b: book generation → refinement  (runs after approval)

Steps are sequential within each phase; no step calls another directly.
"""
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.log_service import AILogService
from app.services.pipeline.parsing import run_parsing
from app.services.pipeline.prd_generator import run_prd_generation
from app.services.pipeline.refiner import run_refinement
from app.services.pipeline.structuring import run_structuring
from app.services.pipeline.book_generator import run_book_generation
from app.services.pipeline.types import (
    PRDSchema,
    ParsedDocumentSchema,
    PipelineContext,
    RefinedBookSchema,
    StructuredContentSchema,
)


@dataclass
class PhaseAResult:
    """Output of the parse-structure-PRD phase, ready for human review."""
    parsed: ParsedDocumentSchema
    structured: StructuredContentSchema
    prd: PRDSchema
    phase: str = "pending_approval"


@dataclass
class PhaseBResult:
    """Output of the book-generation-refinement phase."""
    refined_book: RefinedBookSchema
    phase: str = "complete"


class AIService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._log_svc = AILogService()

    async def phase_a(
        self,
        raw_text: str,
        project_id: UUID,
        user_id: UUID | None = None,
        model_alias: str = "claude-sonnet",
    ) -> PhaseAResult:
        """Steps 1-3: parse → structure → generate PRD.

        The returned PRD must be approved by a human before phase_b is called.
        """
        ctx = PipelineContext(
            project_id=project_id,
            user_id=user_id,
            raw_text=raw_text,
            model_alias=model_alias,
            db=self._db,
        )

        parsed = await run_parsing(ctx, self._log_svc)
        structured = await run_structuring(ctx, parsed, self._log_svc)
        prd = await run_prd_generation(ctx, structured, self._log_svc)

        return PhaseAResult(parsed=parsed, structured=structured, prd=prd)

    async def phase_b(
        self,
        raw_text: str,
        approved_prd: PRDSchema,
        project_id: UUID,
        user_id: UUID | None = None,
        model_alias: str = "claude-sonnet",
    ) -> PhaseBResult:
        """Steps 5-6: generate book from approved PRD → refine.

        raw_text is needed again to re-chunk and select source material per chapter.
        """
        ctx = PipelineContext(
            project_id=project_id,
            user_id=user_id,
            raw_text=raw_text,
            model_alias=model_alias,
            db=self._db,
        )

        # Re-chunk so book_generator can select relevant passages
        from app.ai import TextChunker
        ctx.chunks = TextChunker().split(raw_text)

        book = await run_book_generation(ctx, approved_prd, self._log_svc)
        refined = await run_refinement(ctx, book, approved_prd, self._log_svc)

        return PhaseBResult(refined_book=refined)
