from abc import ABC, abstractmethod
from typing import List
from .base import BaseModel


class BaseAPIModel(BaseModel):
    is_api: bool = True

    def __init__(self, path: str, max_seq_len: int = 2048):
        super().__init__(path, max_seq_len)

    @abstractmethod
    def generate(self, prompt: str, max_out_len: int = 512) -> str:
        """
        Generate response for a single prompt.

        Args:
            prompt: Input prompt string
            max_out_len: Maximum output length

        Returns:
            Generated response string
        """
        pass

    def batch_generate(self, prompts: List[str], max_out_len: int = 512) -> List[str]:
        """
        Generate responses for multiple prompts.

        Args:
            prompts: List of input prompt strings
            max_out_len: Maximum output length per response

        Returns:
            List of generated response strings
        """
        return [self.generate(prompt, max_out_len) for prompt in prompts]
