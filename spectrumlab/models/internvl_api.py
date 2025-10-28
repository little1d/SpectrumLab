from typing import Optional, Union, Dict, Any
from .base_api import BaseAPIModel
from spectrumlab.config import Config
from openai import OpenAI


class InternVL(BaseAPIModel):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs,
    ):
        config = Config()

        # Use provided parameters or fall back to config
        self.api_key = api_key or config.internvl_api_key
        self.base_url = base_url or config.internvl_base_url
        self.model_name = model_name or config.internvl_model_name

        # Validate that we have required configuration
        if not self.api_key:
            raise ValueError(
                "InternVL API key not found. Please set INTERNVL_API_KEY in your .env file "
                "or provide api_key parameter."
            )

        # Ensure base_url has proper protocol for OpenRouter/API services
        if self.base_url and not self.base_url.startswith(("http://", "https://")):
            self.base_url = f"https://{self.base_url}"

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        # Initialize parent class
        super().__init__(model_name=self.model_name, **kwargs)

    def generate(
        self,
        prompt: Union[str, Dict[str, Any]],
        max_tokens: int = 512,
        **generation_kwargs,
    ) -> str:
        """
        Generate response supporting both text and multimodal input.

        Args:
            prompt: Either text string or multimodal dict
            max_tokens: Maximum tokens to generate
            **generation_kwargs: Additional generation parameters like temperature, top_p, etc.

        Returns:
            Generated response string
        """

        # Link: https://internlm.intern-ai.org.cn/api/document
        messages = []

        if isinstance(prompt, dict) and "images" in prompt:
            content = []

            content.append({"type": "text", "text": prompt["text"]})

            for image_data in prompt["images"]:
                content.append(image_data)

            messages.append({"role": "user", "content": content})
        else:
            text_content = prompt if isinstance(prompt, str) else prompt.get("text", "")
            messages.append({"role": "user", "content": text_content})

        # Prepare API call parameters
        api_params = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
        }

        # Add any additional generation parameters
        api_params.update(generation_kwargs)

        try:
            response = self.client.chat.completions.create(**api_params)
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"InternVL API call failed: {e}")
