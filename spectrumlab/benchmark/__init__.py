from .signal_group import SignalGroup
from .perception_group import PerceptionGroup
from .generation_group import GenerationGroup
from .semantic_group import SemanticGroup

__all__ = [
    "SignalGroup",
    "PerceptionGroup",
    "GenerationGroup",
    "SemanticGroup",
    "get_benchmark_group",
]


def get_benchmark_group(level: str, path: str = "./data"):
    level_map = {
        "signal": SignalGroup,
        "perception": PerceptionGroup,
        "semantic": SemanticGroup,
        "generation": GenerationGroup,
    }

    level_lower = level.lower()
    if level_lower not in level_map:
        raise ValueError(f"不支持的评估级别: {level}. 可选值: {list(level_map.keys())}")

    return level_map[level_lower](path=path)
