import time

from openai import AsyncOpenAI

from app.ai.base_client import AIResponse, BaseAIClient
from app.core.settings import settings


class OpenAIProvider(BaseAIClient):
    provider_name = "openai"

    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def complete(
        self,
        prompt: str,
        system: str,
        model: str,
        max_tokens: int,
        temperature: float,
    ) -> AIResponse:
        t0 = time.monotonic()

        response = await self._client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )

        latency_ms = int((time.monotonic() - t0) * 1000)
        usage = response.usage
        content = response.choices[0].message.content or ""

        return AIResponse(
            content=content,
            tokens_input=usage.prompt_tokens if usage else 0,
            tokens_output=usage.completion_tokens if usage else 0,
            model=model,
            provider=self.provider_name,
            latency_ms=latency_ms,
            cached_tokens=0,
            prompt_sent=prompt,
        )
