from app.ai.prompts import ANTI_HALLUCINATION_RULE

SYSTEM = f"""You are a precise document analysis AI. Your task is to extract structure from raw text.
{ANTI_HALLUCINATION_RULE}"""

SINGLE_DOC = """Analyze the document below and return a JSON object with this exact schema:

{{
  "title": "<string or null>",
  "sections": [
    {{
      "title": "<string or null>",
      "content": "<verbatim or lightly cleaned section text>"
    }}
  ]
}}

DOCUMENT:
{text}"""

CHUNK = """This is chunk {index} of {total} from a larger document.
Extract the sections present in THIS chunk only. Return JSON:

{{
  "title": "<string or null — only if visible in this chunk>",
  "sections": [
    {{
      "title": "<string or null>",
      "content": "<section text from this chunk>"
    }}
  ]
}}

CHUNK TEXT:
{text}"""
