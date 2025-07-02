from abc import ABC, abstractmethod
from typing import List
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
    def generate(self, prompt: str, max_out_len: int = 512) -> str:
        pass
