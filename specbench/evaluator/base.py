from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseEvaluator(ABC):

    @abstractmethod
    def evaluate(self, data: List[Dict]) -> Dict:
        pass
