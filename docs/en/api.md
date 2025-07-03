# API Reference

API documentation for Spectral-Hub.

## Core Classes

### SpectralModel

The main model class.

```python
class SpectralModel:
    def __init__(self, model_type='default'):
        pass
    
    def train(self, data):
        """Train the model"""
        pass
    
    def predict(self, input_data):
        """Make predictions"""
        pass
```

## Utility Functions

### load_dataset

```python
def load_dataset(name: str):
    """Load dataset"""
    pass
```

### evaluate_model

```python
def evaluate_model(model, test_data):
    """Evaluate model performance"""
    pass
```

## Related Links

- [Tutorial](/en/tutorial)
- [Benchmark](/en/benchmark)
