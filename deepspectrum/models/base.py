from abc import ABC, abstractmethod
from typing import Union, Any, Dict


class BaseModel(ABC):
    is_api: bool = False

    def __init__(self, path: str, max_seq_len: int = 2048):
        self.path = path
        self.max_seq_len = max_seq_len

    @abstractmethod
    def generate(
        self, prompt: Union[str, Dict[str, Any]], max_out_len: int = 512
    ) -> str:
        """
        Generate response for a single prompt.

        Args:
            prompt: Input prompt, can be:
                   - str: Simple text prompt
                   - Dict: Multimodal prompt with format:
                     {
                         "text": "question text",
                         "images": [{"type": "image_url", "image_url": {"url": "data:..."}}]
                     }
            max_out_len: Maximum output length

        Returns:
            Generated response string
        """
        pass
