#!/usr/bin/env python3
"""
Development installation script for SpectrumLab.
This script installs the package in development mode.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def main():
    print("🚀 Installing SpectrumLab in development mode...")
    
    # Check if we're in the right directory
    if not os.path.exists("spectrumlab"):
        print("❌ Error: spectrumlab directory not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install in development mode
    if not run_command("pip install -e .", "Installing package in development mode"):
        print("❌ Installation failed. Please check the error messages above.")
        sys.exit(1)
    
    # Test import
    print("🧪 Testing imports...")
    try:
        import spectrumlab
        from spectrumlab.models import Claude
        from spectrumlab.config import Config
        print("✅ All imports successful!")
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        print("💡 Try running: python -m pytest tests/test_import.py")
        sys.exit(1)
    
    print("\n🎉 SpectrumLab development environment setup complete!")
    print("💡 You can now run tests with: python -m pytest tests/")

if __name__ == "__main__":
    main() 