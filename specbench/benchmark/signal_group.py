from typing import List, Dict, Optional, Union
from specbench.evaluator.choice_evaluator import ChoiceEvaluator
from .base import BaseGroup


class SignalGroup(BaseGroup):
    def __init__(self, level: str, path: str = "./data"):
        super().__init__(level, path)
