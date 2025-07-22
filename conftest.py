"""
Pytest configuration file for SpectrumLab project.
This ensures the spectrumlab module is available for all tests.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir)) 