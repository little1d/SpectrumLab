"""
SpectrumLab - Comprehensive toolkit for spectroscopy deep learning.

This package provides tools for dataset loading, training, evaluation, 
inference, and more for spectroscopy applications.
"""

__version__ = "0.0.1"
__author__ = "Zhuo Yang, Tianfan Fu"

# Import main modules
from . import models
from . import config
from . import evaluator
from . import benchmark
from . import utils
from . import cli

# Export main classes for convenience
from .models import DeepSeek, GPT4o, InternVL
from .models import Claude_Sonnet_3_5, Claude_Opus_4, Claude_Haiku_3_5, Claude_Sonnet_4
from .models import GPT4_1, GPT4_Vision
from .models import Grok_2_Vision
from .models import Gemini_2_5_Pro
from .config import Config

__all__ = [
    "models",
    "config", 
    "evaluator",
    "benchmark",
    "utils",
    "cli",
    "DeepSeek",
    "GPT4o", 
    "InternVL",
    "Claude_Sonnet_3_5",
    "Claude_Opus_4",
    "Claude_Haiku_3_5",
    "Claude_Sonnet_4",
    "GPT4_1",
    "GPT4_Vision",
    "Grok_2_Vision",
    "Gemini_2_5_Pro",
    "Config",
] 