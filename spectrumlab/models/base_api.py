from abc import abstractmethod
from typing import Dict, Any, Union
from .base import BaseModel


class BaseAPIModel(BaseModel):
    is_api: bool = True

    def __init__(self, model_name: str = "api_model", max_seq_len: int = 2048):
        """
        Initialize API model.

        Args:
            model_name: Name of the model
            max_seq_len: Maximum sequence length
        """
        super().__init__(path=model_name, max_seq_len=max_seq_len)

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
