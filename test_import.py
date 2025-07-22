#!/usr/bin/env python3
"""
Simple test script to verify spectrumlab module imports work correctly.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    print("Testing spectrumlab imports...")
    
    # Test basic imports
    from spectrumlab import Config
    print("✅ Config import successful")
    
    from spectrumlab.models import Claude
    print("✅ Claude model import successful")
    
    from spectrumlab.utils.image_utils import encode_image_to_base64
    print("✅ image_utils import successful")
    
    from spectrumlab.benchmark.signal_group import SignalGroup
    print("✅ signal_group import successful")
    
    from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator
    print("✅ choice_evaluator import successful")
    
    print("\n🎉 All imports successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1) 