"""
Simple test to verify that spectrumlab module can be imported correctly.
"""

def test_spectrumlab_import():
    """Test that spectrumlab module can be imported."""
    try:
        from spectrumlab.models import Claude
        assert Claude is not None
    except ImportError as e:
        raise ImportError(f"Failed to import spectrumlab.models.Claude: {e}")

def test_config_import():
    """Test that Config can be imported."""
    try:
        from spectrumlab.config import Config
        assert Config is not None
    except ImportError as e:
        raise ImportError(f"Failed to import spectrumlab.config.Config: {e}") 