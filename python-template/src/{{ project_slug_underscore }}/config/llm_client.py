"""Pydantic AI model factory."""

from pydantic_ai.models import Model

from {{ project_slug_underscore }}.config import get_settings


def build_llm() -> Model:
    s = get_settings()
    if s.llm_provider == "anthropic":
        from pydantic_ai.models.anthropic import AnthropicModel
        from pydantic_ai.providers.anthropic import AnthropicProvider
        return AnthropicModel(s.model_id, provider=AnthropicProvider(api_key=s.anthropic_api_key))
    if s.llm_provider == "openai":
        from pydantic_ai.models.openai import OpenAIModel
        from pydantic_ai.providers.openai import OpenAIProvider
        return OpenAIModel(s.openai_model_id, provider=OpenAIProvider(api_key=s.openai_api_key))
    if s.llm_provider == "bedrock":
        from pydantic_ai.models.bedrock import BedrockConverseModel
        return BedrockConverseModel(s.bedrock_model_id)
    raise ValueError(f"Unsupported provider: {s.llm_provider}")
