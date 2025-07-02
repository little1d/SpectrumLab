from .base import BaseGroup


class PerceptionGroup(BaseGroup):
    def __init__(self, path: str = "./data"):
        super().__init__(level="Perception", path=path)
