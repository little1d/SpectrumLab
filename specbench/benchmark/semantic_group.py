from .base import BaseGroup


class SemanticGroup(BaseGroup):
    def __init__(self, path: str = "./data"):
        super().__init__(level="Semantic", path=path)
