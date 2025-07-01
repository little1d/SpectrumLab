from abc import ABC, abstractmethod
from typing import List
from .base import BaseModel


class BaseAPIModel(BaseModel):
    is_api: bool = True

    def __init__(self, path: str, max_seq_len: int = 2048):
        super().__init__(path, max_seq_len)

    @abstractmethod
    def generate(self, inputs: List[str], max_out_len: int) -> List[str]:
        pass
