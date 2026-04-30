from app.ai.prompts import ANTI_HALLUCINATION_RULE

SYSTEM = f"""You are an expert editorial analyst and book architect.
Your task is to analyze parsed document sections and build an editorial structure.
{ANTI_HALLUCINATION_RULE}"""

PROMPT = """Based ONLY on the sections below, return a JSON object with this schema:

{{
  "theme": "<central theme of the work>",
  "target_audience": "<inferred audience>",
  "genre": "<genre or category>",
  "tone": "<formal | informal | technical | narrative | didactic>",
  "key_messages": ["<message 1>", "..."],
  "chapters": [
    {{
      "title": "<proposed chapter title>",
      "summary": "<what this chapter covers>",
      "key_points": ["<point 1>", "..."],
      "target_words": <integer estimate>
    }}
  ]
}}

PARSED SECTIONS:
{sections_text}"""
