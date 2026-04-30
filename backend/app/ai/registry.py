from dataclasses import dataclass

from app.ai.base_client import BaseAIClient

# Lazy singletons — instantiated once per process.
_instances: dict[str, BaseAIClient] = {}


@dataclass(frozen=True)
class ModelConfig:
    alias: str
    provider: str          # "anthropic" | "openai"
    model_id: str
    max_tokens: int
    supports_caching: bool
    cost_input_per_1k: float   # USD
    cost_output_per_1k: float  # USD


MODELS: dict[str, ModelConfig] = {
    # ── Anthropic ──────────────────────────────────────────────
    "claude-sonnet": ModelConfig(
        alias="claude-sonnet",
        provider="anthropic",
        model_id="claude-sonnet-4-6",
        max_tokens=8192,
        supports_caching=True,
        cost_input_per_1k=0.003,
        cost_output_per_1k=0.015,
    ),
    "claude-haiku": ModelConfig(
        alias="claude-haiku",
        provider="anthropic",
        model_id="claude-haiku-4-5-20251001",
        max_tokens=4096,
        supports_caching=True,
        cost_input_per_1k=0.00025,
        cost_output_per_1k=0.00125,
    ),
    # ── OpenAI ─────────────────────────────────────────────────
    "gpt-4o": ModelConfig(
        alias="gpt-4o",
        provider="openai",
        model_id="gpt-4o",
        max_tokens=8192,
        supports_caching=False,
        cost_input_per_1k=0.005,
        cost_output_per_1k=0.015,
    ),
    "gpt-4o-mini": ModelConfig(
        alias="gpt-4o-mini",
        provider="openai",
        model_id="gpt-4o-mini",
        max_tokens=4096,
        supports_caching=False,
        cost_input_per_1k=0.00015,
        cost_output_per_1k=0.0006,
    ),
}


def get_model_config(alias: str) -> ModelConfig:
    try:
        return MODELS[alias]
    except KeyError:
        available = ", ".join(MODELS)
        raise ValueError(f"Unknown model alias '{alias}'. Available: {available}")


def get_client(alias: str) -> BaseAIClient:
    if alias in _instances:
        return _instances[alias]

    config = get_model_config(alias)

    if config.provider == "anthropic":
        from app.ai.providers.anthropic_provider import AnthropicProvider
        client: BaseAIClient = AnthropicProvider()
    elif config.provider == "openai":
        from app.ai.providers.openai_provider import OpenAIProvider
        client = OpenAIProvider()
    else:
        raise ValueError(f"Unknown provider '{config.provider}'")

    _instances[alias] = client
    return client


def estimate_cost(config: ModelConfig, tokens_in: int, tokens_out: int) -> float:
    return (tokens_in / 1000 * config.cost_input_per_1k) + (
        tokens_out / 1000 * config.cost_output_per_1k
    )
