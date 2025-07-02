from typing import List, Dict, Any, Optional
from .base_api import BaseAPIModel
from specbench.config import Config


class DeepSeekAPI(BaseAPIModel):
    """
    DeepSeek API model implementation.

    Uses simplified configuration system to load API credentials and settings.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs,
    ):
        config = Config()

        # Use provided parameters or fall back to config
        self.api_key = api_key or config.deepseek_api_key
        self.base_url = base_url or config.deepseek_base_url
        self.model_name = model_name or config.deepseek_model_name

        # Validate that we have required configuration
        if not self.api_key:
            raise ValueError(
                "DeepSeek API key not found. Please set DEEPSEEK_API_KEY in your .env file "
                "or provide api_key parameter."
            )

        # Initialize parent class
        super().__init__(path=self.model_name, **kwargs)

        print(f"DeepSeek API initialized:")
        print(f"  Model: {self.model_name}")
        print(f"  Base URL: {self.base_url}")
        print(f"  API Key: {'✓ SET' if self.api_key else '✗ NOT SET'}")

    def generate(self, prompt: str, max_out_len: int = 512) -> str:
        # TODO: Implement actual API call logic
        # For now, return a placeholder response

        print(f"[DeepSeek API] Generating response for prompt (length: {len(prompt)})")
        print(f"[DeepSeek API] Using model: {self.model_name}")
        print(f"[DeepSeek API] Max output length: {max_out_len}")

        # Placeholder response
        return f"[DeepSeek Response] This is a placeholder response for the prompt: {prompt[:100]}..."

    def batch_generate(self, prompts: List[str], max_out_len: int = 512) -> List[str]:
        print(f"[DeepSeek API] Batch generating {len(prompts)} responses")
        return super().batch_generate(prompts, max_out_len)
