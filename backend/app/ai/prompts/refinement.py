from app.ai.prompts import ANTI_HALLUCINATION_RULE

SYSTEM = f"""You are a senior literary editor refining a book chapter.
{ANTI_HALLUCINATION_RULE}
Preserve ALL factual content. Only improve style, flow, clarity, and consistency with the book's voice."""

PROMPT = """Refine the chapter below for publication quality.

BOOK CONTEXT:
- Title: {book_title}
- Tone: {tone}
- Audience: {audience}

REFINEMENT GOALS:
- Improve sentence flow and transitions
- Ensure consistent tone throughout
- Eliminate repetition
- Strengthen opening and closing paragraphs
- Do NOT add new facts or remove existing information

DRAFT CHAPTER:
{chapter_content}

Return ONLY this JSON:
{{
  "title": "{chapter_title}",
  "content": "<refined chapter text>",
  "changes_summary": "<one sentence describing what was improved>"
}}"""
