from .base import BaseGroup


class GenerationGroup(BaseGroup):
    def __init__(self, path: str = "./data"):
        super().__init__(level="Generation", path=path)
