from typing import Optional, Union, Dict, Any
from .base_api import BaseAPIModel
from spectrumlab.config import Config
from openai import OpenAI


class Claude_Sonnet_3_5(BaseAPIModel):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs,
    ):
        config = Config()

        # Use provided parameters or fall back to config
        self.api_key = api_key or config.BOYUE_API_KEY
        self.base_url = base_url or config.BOYUE_BASE_URL
        self.model_name = model_name or config.claude_sonnet_3_5_model_name

        # Validate that we have required configuration
        if not self.api_key:
            raise ValueError(
                "Claude API key not found. Please set CLAUDE_API_KEY in your .env file "
                "or provide api_key parameter."
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        # Initialize parent class
        super().__init__(model_name=self.model_name, **kwargs)

    def generate(
        self, prompt: Union[str, Dict[str, Any]], max_out_len: int = 512
    ) -> str:
        """
        Generate response supporting both text and multimodal input.

        Args:
            prompt: Either text string or multimodal dict
            max_out_len: Maximum tokens to generate

        Returns:
            Generated response string
        """

        # Link: https://docs.anthropic.com/claude/reference/getting-started-with-the-api
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

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_out_len,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Claude API call failed: {e}")


class Claude_Opus_4(BaseAPIModel):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs,
    ):
        config = Config()

        # Use provided parameters or fall back to config
        self.api_key = api_key or config.BOYUE_API_KEY
        self.base_url = base_url or config.BOYUE_BASE_URL
        self.model_name = model_name or config.claude_opus_4_model_name

        # Validate that we have required configuration
        if not self.api_key:
            raise ValueError(
                "Claude API key not found. Please set CLAUDE_API_KEY in your .env file "
                "or provide api_key parameter."
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        # Initialize parent class
        super().__init__(model_name=self.model_name, **kwargs)

    def generate(
        self, prompt: Union[str, Dict[str, Any]], max_out_len: int = 512
    ) -> str:
        """
        Generate response supporting both text and multimodal input.

        Args:
            prompt: Either text string or multimodal dict
            max_out_len: Maximum tokens to generate

        Returns:
            Generated response string
        """

        # Link: https://docs.anthropic.com/claude/reference/getting-started-with-the-api
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

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_out_len,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Claude API call failed: {e}")


class Claude_Haiku_3_5(BaseAPIModel):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs,
    ):
        config = Config()

        # Use provided parameters or fall back to config
        self.api_key = api_key or config.BOYUE_API_KEY
        self.base_url = base_url or config.BOYUE_BASE_URL
        self.model_name = model_name or config.claude_haiku_3_5_model_name

        # Validate that we have required configuration
        if not self.api_key:
            raise ValueError(
                "Claude API key not found. Please set CLAUDE_API_KEY in your .env file "
                "or provide api_key parameter."
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        # Initialize parent class
        super().__init__(model_name=self.model_name, **kwargs)

    def generate(
        self, prompt: Union[str, Dict[str, Any]], max_out_len: int = 512
    ) -> str:
        """
        Generate response supporting both text and multimodal input.

        Args:
            prompt: Either text string or multimodal dict
            max_out_len: Maximum tokens to generate

        Returns:
            Generated response string
        """

        # Link: https://docs.anthropic.com/claude/reference/getting-started-with-the-api
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

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_out_len,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Claude API call failed: {e}")

class Claude_Sonnet_4(BaseAPIModel):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs,
    ):
        config = Config()

        # Use provided parameters or fall back to config
        self.api_key = api_key or config.BOYUE_API_KEY
        self.base_url = base_url or config.BOYUE_BASE_URL
        self.model_name = model_name or config.claude_sonnet_4_model_name

        # Validate that we have required configuration
        if not self.api_key:
            raise ValueError(
                "Claude API key not found. Please set CLAUDE_API_KEY in your .env file "
                "or provide api_key parameter."
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        # Initialize parent class
        super().__init__(model_name=self.model_name, **kwargs)

    def generate(
        self, prompt: Union[str, Dict[str, Any]], max_out_len: int = 512
    ) -> str:
        """
        Generate response supporting both text and multimodal input.

        Args:
            prompt: Either text string or multimodal dict
            max_out_len: Maximum tokens to generate

        Returns:
            Generated response string
        """

        # Link: https://docs.anthropic.com/claude/reference/getting-started-with-the-api
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

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_out_len,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Claude API call failed: {e}")

