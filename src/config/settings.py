from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()


class LLMProviderSettings(BaseSettings):
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3

class GithubOpenAISettings(LLMProviderSettings):
    api_key: str = os.getenv("GITHUB_MODELS_API_KEY")
    default_model: str = "openai/gpt-4.1-mini"
    base_url: str = "https://models.github.ai/inference"

class DeepSeekSettings(LLMProviderSettings):
    api_key: str = os.getenv("DEEPSEEK_API_KEY")
    default_model: str = "deepseek-chat"
    base_url: str = "https://api.deepseek.com"


class OpenAISettings(LLMProviderSettings):
    api_key: str = os.getenv("OPENAI_API_KEY")
    default_model: str = "gpt-4o"


class AnthropicSettings(LLMProviderSettings):
    api_key: str = os.getenv("ANTHROPIC_API_KEY")
    default_model: str = "claude-3-5-sonnet-20240620"
    max_tokens: int = 1024


class LlamaSettings(LLMProviderSettings):
    api_key: str = "key"  # required, but not used
    default_model: str = "llama3"
    base_url: str = "http://localhost:11434/v1"


class Settings(BaseSettings):
    app_name: str = "GenAI Project Template"
    openai: OpenAISettings = OpenAISettings()
    anthropic: AnthropicSettings = AnthropicSettings()
    llama: LlamaSettings = LlamaSettings()
    github_models: GithubOpenAISettings = GithubOpenAISettings()
    deepseek: DeepSeekSettings = DeepSeekSettings()

@lru_cache
def get_settings():
    return Settings()