"""Shared types for the AI pipeline.

Pydantic schemas here serve dual purpose:
  - Validate AI JSON output (anti-hallucination gate)
  - Act as typed data transfer objects between pipeline steps
"""
from dataclasses import dataclass, field
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.chunker import Chunk


# ── Pipeline execution context ────────────────────────────────

@dataclass
class PipelineContext:
    project_id: UUID
    user_id: UUID | None
    raw_text: str
    model_alias: str
    db: AsyncSession
    chunks: list[Chunk] = field(default_factory=list)


# ── Step 1 — Parsing ──────────────────────────────────────────

class ParsedSectionSchema(BaseModel):
    title: str | None = None
    content: str


class ParsedDocumentSchema(BaseModel):
    title: str | None = None
    sections: list[ParsedSectionSchema] = Field(default_factory=list)


# ── Step 2 — Structuring ──────────────────────────────────────

class ChapterOutlineSchema(BaseModel):
    title: str
    summary: str
    key_points: list[str] = Field(default_factory=list)
    target_words: int = 1500


class StructuredContentSchema(BaseModel):
    theme: str
    target_audience: str
    genre: str
    tone: str
    key_messages: list[str] = Field(default_factory=list)
    chapters: list[ChapterOutlineSchema] = Field(default_factory=list)


# ── Step 3 — PRD ──────────────────────────────────────────────

class ChapterSpecSchema(BaseModel):
    number: int
    title: str
    objective: str
    content_requirements: list[str] = Field(default_factory=list)
    estimated_words: int = 1500
    key_sources: list[str] = Field(default_factory=list)


class PRDSchema(BaseModel):
    book_title: str
    subtitle: str | None = None
    objective: str
    target_audience: str
    tone: str
    estimated_total_words: int
    chapters: list[ChapterSpecSchema] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


# ── Step 5 — Book generation ──────────────────────────────────

class GeneratedChapterSchema(BaseModel):
    title: str
    content: str
    word_count: int


class BookSchema(BaseModel):
    title: str
    chapters: list[GeneratedChapterSchema] = Field(default_factory=list)


# ── Step 6 — Refinement ───────────────────────────────────────

class RefinedChapterSchema(BaseModel):
    title: str
    content: str
    changes_summary: str = ""


class RefinedBookSchema(BaseModel):
    title: str
    chapters: list[RefinedChapterSchema] = Field(default_factory=list)
