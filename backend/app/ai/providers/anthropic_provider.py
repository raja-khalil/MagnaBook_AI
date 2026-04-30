import time

import anthropic

from app.ai.base_client import AIResponse, BaseAIClient
from app.core.settings import settings

# Minimum character count to justify attaching a cache_control block.
_CACHE_THRESHOLD = 1024


class AnthropicProvider(BaseAIClient):
    provider_name = "anthropic"

    def __init__(self) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def complete(
        self,
        prompt: str,
        system: str,
        model: str,
        max_tokens: int,
        temperature: float,
    ) -> AIResponse:
        system_blocks = self._build_system(system)
        t0 = time.monotonic()

        message = await self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_blocks,
            messages=[{"role": "user", "content": prompt}],
        )

        latency_ms = int((time.monotonic() - t0) * 1000)
        usage = message.usage
        cached = getattr(usage, "cache_read_input_tokens", 0) or 0

        return AIResponse(
            content=message.content[0].text,
            tokens_input=usage.input_tokens,
            tokens_output=usage.output_tokens,
            model=model,
            provider=self.provider_name,
            latency_ms=latency_ms,
            cached_tokens=cached,
            prompt_sent=prompt,
        )

    @staticmethod
    def _build_system(system: str) -> list[dict]:
        """Wrap system prompt with cache_control when it is large enough."""
        block: dict = {"type": "text", "text": system}
        if len(system) >= _CACHE_THRESHOLD:
            block["cache_control"] = {"type": "ephemeral"}
        return [block]
