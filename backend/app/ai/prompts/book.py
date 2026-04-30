from app.ai.prompts import ANTI_HALLUCINATION_RULE

SYSTEM = f"""You are an expert ghostwriter producing a book chapter.
{ANTI_HALLUCINATION_RULE}
Write ONLY from the source material provided. Match the tone and audience defined in the chapter spec."""

PROMPT = """Write chapter {chapter_number}: "{chapter_title}" using the specification and source material below.

CHAPTER SPECIFICATION:
- Objective: {objective}
- Tone: {tone}
- Target audience: {audience}
- Estimated words: {estimated_words}
- Content requirements:
{requirements_list}

SOURCE MATERIAL (use ONLY this content — do not add facts not present here):
{source_chunks}

Return ONLY this JSON:
{{
  "title": "{chapter_title}",
  "content": "<full chapter text, well-structured with subheadings>",
  "word_count": <integer>
}}"""
