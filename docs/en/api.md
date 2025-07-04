# API Reference

Detailed API documentation for SpectrumLab.

## Benchmark Module

### get_benchmark_group(level)

Get a benchmark group for the specified level.

```python
from spectrumlab.benchmark import get_benchmark_group

# Get perception group
benchmark = get_benchmark_group("perception")

# Get semantic group
benchmark = get_benchmark_group("semantic")

# Get generation group
benchmark = get_benchmark_group("generation")

# Get signal group
benchmark = get_benchmark_group("signal")
```

### BaseGroup Class

#### get_data_by_subcategories(subcategories)

Get data by subcategories.

**Parameters:**

- `subcategories` (str | List[str] | "all"): Subcategory name or list

**Returns:**

- `List[Dict]`: List of data items

```python
# Get all subcategory data
data = benchmark.get_data_by_subcategories("all")

# Get specific subcategory data
data = benchmark.get_data_by_subcategories(["IR_spectroscopy", "Raman_spectroscopy"])

# Get single subcategory data
data = benchmark.get_data_by_subcategories("IR_spectroscopy")
```

#### get_available_subcategories()

Get all available subcategories.

**Returns:**

- `List[str]`: List of available subcategories

```python
subcategories = benchmark.get_available_subcategories()
print(subcategories)
```

## Evaluator Module

### get_evaluator(level)

Get an evaluator for the specified level.

```python
from spectrumlab.evaluator import get_evaluator

evaluator = get_evaluator("perception")
```

### BaseEvaluator Class

#### evaluate(data_items, model, max_out_len=512, batch_size=None, save_path="./eval_results")

Run evaluation.

**Parameters:**

- `data_items` (List[Dict]): List of data items
- `model`: Model object
- `max_out_len` (int): Maximum output length
- `batch_size` (int, optional): Batch size (not implemented yet)
- `save_path` (str): Path to save results

**Returns:**

- `Dict`: Evaluation results

```python
results = evaluator.evaluate(
    data_items=data,
    model=model,
    max_out_len=512,
    save_path="./eval_results"
)
```

### ChoiceEvaluator Class

Inherits from BaseEvaluator, specifically for multiple choice evaluation.

- Supports multimodal input (image + text)
- Extracts predictions using `\box{}` format
- Uses MMAR-based string matching algorithm

## Models Module

### GPT4oAPI Class

OpenAI GPT-4o model interface.

```python
from spectrumlab.models import GPT4oAPI

model = GPT4oAPI()
```

**Environment Variables:**

- `OPENAI_API_KEY`: OpenAI API key

### DeepSeekAPI Class

DeepSeek model interface.

```python
from spectrumlab.models import DeepSeekAPI

model = DeepSeekAPI()
```

**Environment Variables:**

- `DEEPSEEK_API_KEY`: DeepSeek API key

### InternVLAPI Class

InternVL model interface.

```python
from spectrumlab.models import InternVLAPI

model = InternVLAPI()
```

**Environment Variables:**

- `INTERNVL_API_KEY`: InternVL API key

## Utils Module

### Image Processing

#### prepare_images_for_prompt(image_paths)

Prepare image data for prompts.

**Parameters:**

- `image_paths` (List[str]): List of image paths

**Returns:**

- `List[Dict]`: List of image data

#### normalize_image_paths(image_paths_field)

Normalize image paths.

**Parameters:**

- `image_paths_field`: Image paths field

**Returns:**

- `List[str]`: List of normalized image paths

## Data Structures

### Data Item Format

Each data item contains the following fields:

```python
{
    "question": str,           # Question text
    "choices": List[str],      # List of choices
    "answer": str,             # Correct answer
    "image_path": str,         # Image path (optional)
    "category": str,           # Category
    "sub_category": str        # Subcategory
}
```

### Evaluation Results Format

```python
{
    "metrics": {
        "overall": {
            "accuracy": float,      # Overall accuracy
            "correct": int,         # Number of correct answers
            "total": int,           # Total number of questions
            "no_prediction_count": int  # Number of no predictions
        },
        "category_metrics": {
            "category_name": {
                "accuracy": float,
                "correct": int,
                "total": int
            }
        },
        "subcategory_metrics": {
            "subcategory_name": {
                "accuracy": float,
                "correct": int,
                "total": int
            }
        }
    },
    "saved_files": List[str],   # List of saved file paths
    "total_items": int          # Total number of data items
}
```

## Custom Extensions

### Custom Evaluator

```python
from spectrumlab.evaluator.base import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def _build_prompt(self, item: Dict) -> str:
        """Build prompt"""
        # Custom logic
        pass
    
    def _extract_prediction(self, response: str, item: Dict) -> str:
        """Extract prediction"""
        # Custom logic
        pass
    
    def _calculate_accuracy(self, answer: str, prediction: str, item: Dict) -> bool:
        """Calculate accuracy"""
        # Custom logic
        pass
```

### Custom Model

```python
from spectrumlab.models.base import BaseModel

class CustomModel(BaseModel):
    def generate(self, prompt, max_out_len=512):
        """Generate response"""
        # Custom logic
        pass
```

## Related Links

- [Tutorial](/en/tutorial)
- [Benchmark](/en/benchmark)
