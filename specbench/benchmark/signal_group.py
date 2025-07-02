from .base import BaseGroup


class SignalGroup(BaseGroup):
    def __init__(self, path: str = "./data"):
        super().__init__(level="Signal", path=path)
