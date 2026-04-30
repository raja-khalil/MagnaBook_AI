from app.ai.prompts import ANTI_HALLUCINATION_RULE

SYSTEM = f"""You are a senior book product manager creating a detailed specification for editorial production.
{ANTI_HALLUCINATION_RULE}
Every chapter spec must reflect content actually present in the source analysis."""

PROMPT = """Based on the editorial analysis below, produce a detailed PRD (Product Requirements Document) for this book.
Return ONLY this JSON schema:

{{
  "book_title": "<definitive title>",
  "subtitle": "<subtitle or null>",
  "objective": "<one-paragraph statement of what the book achieves>",
  "target_audience": "<precise audience definition>",
  "tone": "<writing tone>",
  "estimated_total_words": <integer>,
  "chapters": [
    {{
      "number": <integer>,
      "title": "<chapter title>",
      "objective": "<what the reader gains from this chapter>",
      "content_requirements": ["<specific content item 1>", "..."],
      "estimated_words": <integer>,
      "key_sources": ["<relevant section titles from source>"]
    }}
  ],
  "constraints": ["<editorial constraint 1>", "..."]
}}

EDITORIAL ANALYSIS:
{structured_text}"""
