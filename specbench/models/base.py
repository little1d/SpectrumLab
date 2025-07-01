from abc import ABC, abstractmethod
from typing import List


class BaseModel(ABC):
    is_api: bool = False

    def __init__(self, path: str, max_seq_len: int = 2048):
        self.path = path
        self.max_seq_len = max_seq_len

    @abstractmethod
    def generate(self, prompts: str, max_out_len: int = 512) -> List[str]:
        pass

    def batch_generate(self, prompts: List[str], max_out_len: int = 512) -> List[str]:
        return [self.generate(prompt, max_out_len) for prompt in prompts]
