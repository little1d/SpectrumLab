"""
Pytest configuration file for SpectrumLab tests.
This file sets up the Python path to include the project root.
"""

import sys
import os
from pathlib import Path

# Get the project root directory (parent of tests directory)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Also add the project root to PYTHONPATH environment variable
os.environ['PYTHONPATH'] = str(project_root) + os.pathsep + os.environ.get('PYTHONPATH', '') 