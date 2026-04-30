import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class PipelineError(Exception):
    pass


@dataclass
class AIResponse:
    content: str
    tokens_input: int
    tokens_output: int
    model: str
    provider: str
    latency_ms: int
    cached_tokens: int = 0
    prompt_sent: str = field(default="", repr=False)


def _extract_json(text: str) -> str:
    """Strip markdown fences and return the first JSON object/array found."""
    # Remove ```json ... ``` fences
    fenced = re.search(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", text, re.DOTALL)
    if fenced:
        return fenced.group(1)
    # Raw JSON object or array
    raw = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if raw:
        return raw.group(1)
    return text


class BaseAIClient(ABC):
    provider_name: str

    @abstractmethod
    async def complete(
        self,
        prompt: str,
        system: str,
        model: str,
        max_tokens: int,
        temperature: float,
    ) -> AIResponse: ...

    async def complete_json(
        self,
        prompt: str,
        system: str,
        schema_cls: type[T],
        model: str,
        max_tokens: int,
        temperature: float = 0.1,
        max_retries: int = 3,
    ) -> tuple[T, AIResponse]:
        """Call the model and validate the JSON response against schema_cls.
        Retries with error feedback on parse/validation failure."""
        last_response: AIResponse | None = None
        retry_suffix = ""

        for attempt in range(max_retries):
            full_prompt = prompt + retry_suffix
            response = await self.complete(full_prompt, system, model, max_tokens, temperature)
            last_response = response

            try:
                json_str = _extract_json(response.content)
                data = json.loads(json_str)
                validated = schema_cls.model_validate(data)
                return validated, response

            except (json.JSONDecodeError, ValidationError, ValueError) as exc:
                if attempt == max_retries - 1:
                    raise PipelineError(
                        f"Model returned invalid JSON after {max_retries} attempts. "
                        f"Last error: {exc}\nRaw response: {response.content[:500]}"
                    ) from exc

                retry_suffix = (
                    f"\n\n[CORRECTION NEEDED — attempt {attempt + 2}/{max_retries}]: "
                    f"Your previous response could not be parsed: {exc}. "
                    "Return ONLY a valid JSON object matching the requested schema. "
                    "No markdown, no prose, no code fences."
                )

        # unreachable, but satisfies type checker
        raise PipelineError("Unexpected retry loop exit")
