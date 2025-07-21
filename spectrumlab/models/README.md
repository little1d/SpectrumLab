# Model Integration & Testing Pipeline

This guide explains how to quickly adapt and test a new multimodal model in SpectrumLab.

## 1. Environment Configuration (`.env`)

Add your model's API keys and endpoints to the `.env` file at the project root. Example:

```
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL_NAME=deepseek-model

GPT4O_API_KEY=your_gpt4o_key
GPT4O_BASE_URL=https://api.gpt4o.com
GPT4O_MODEL_NAME=gpt-4o

INTERNVL_API_KEY=your_internvl_key
INTERNVL_BASE_URL=https://api.internvl.com
INTERNVL_MODEL_NAME=internvl-model
```

## 2. Config Class (`@config`)

Ensure your model's config is added to `spectrumlab/config/base_config.py`:

```python
@dataclass
class Config:
    ...
    yourmodel_api_key: str = os.getenv("YOURMODEL_API_KEY")
    yourmodel_base_url: str = os.getenv("YOURMODEL_BASE_URL")
    yourmodel_model_name: str = os.getenv("YOURMODEL_MODEL_NAME")
```

## 3. Model Registration

Implement your model in `spectrumlab/models/yourmodel_api.py` (inherit from `BaseAPIModel` or `BaseModel`).

Register it in `spectrumlab/models/__init__.py`:

```python
from .yourmodel_api import YourModel
__all__ = [ ..., "YourModel" ]
```

## 4. Add Test File

Create a test file in `tests/models/test_yourmodel.py`. Example:

```python
import pytest
from spectrumlab.models import YourModel
from spectrumlab.utils.image_utils import encode_image_to_base64
from spectrumlab.benchmark.signal_group import SignalGroup
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator

def test_yourmodel_text_generation():
    model = YourModel()
    response = model.generate("What is spectroscopy?")
    assert isinstance(response, str)
    assert len(response) > 0

def test_yourmodel_multimodal_generation():
    model = YourModel()
    image_path = "playground/models/test.png"
    image_base64 = encode_image_to_base64(image_path)
    prompt = {
        "text": "Please explain this spectroscopy image.",
        "images": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
        ],
    }
    response = model.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0

def test_yourmodel_signalgroup_evaluation():
    model = YourModel()
    signal_group = SignalGroup("data")
    data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])
    evaluator = ChoiceEvaluator()
    results = evaluator.evaluate(data_items=data, model=model)
    assert "metrics" in results
    assert "overall" in results["metrics"]
```

## 5. Run Tests

From the project root, run:

```
pytest -s -v tests/models/test_yourmodel.py
```

Or run all model tests:

```
pytest -s -v tests/models/
```

---

**Tip:**

- Each model has its own test file for easy debugging and extension.
- Add new models by following steps 1-4 above.
