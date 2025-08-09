# API Reference

SpectrumLab Provides a concise and powerful API interface to help you quickly build deep learning applications in spectroscopy. This document covers the usage of core modules and guidelines for custom extensions.

## Benchmark Module

Benchmark The module is the core of data access in SpectrumLab, providing a unified interface to load and manage spectroscopic benchmarking data at different levels.

### Get Benchmark Group

The `get_benchmark_group` function can be used to obtain benchmark test groups at four different levels:

```python
from spectrumlab.benchmark import get_benchmark_group

signal_group = get_benchmark_group("signal")        # Signal layer
perception_group = get_benchmark_group("perception")  # Perception layer
semantic_group = get_benchmark_group("semantic")      # Semantic layer
generation_group = get_benchmark_group("generation")  # Generation layer
```

### Data access

Each Benchmark Group provides flexible data access methods:

```python
# Get all data
data = signal_group.get_ data_by_subcategories("all")

# Obtain data for specific sub - categories
data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])

# Get all available sub-categories of the Benchmark Group
subcategories = signal_group.get_available_subcategories()
print(subcategories)
```

**Method description：**

- `get_data_by_subcategories("all")`: Return the data of all sub - categories at this level
- `get_data_by_subcategories([...])`: Return the data list of the specified subcategory
- `get_available_subcategories()`: View the names of all sub - categories contained in the current level

## Model Module

Model The module provides a unified model interface, supporting the integration of various pre-trained models and custom models.

### Use existing models

SpectrumLab Built-in multiple advanced multimodal model interfaces:

```python
from spectrumlab.models import GPT4oAPI

gpt4o = GPT4oAPI()

response = gpt4o.generate("Your Prompts")
```

**Supported models：**

- `GPT4oAPI`: OpenAI GPT-4o
- `ClaudeAPI`: Anthropic Claude series
- `DeepSeekAPI`: DeepSeek-VL
- `QwenVLAPI`: Qwen-VL series
- `InternVLAPI`: InternVL series

### Custom model

By inheriting from the `BaseModel` class, you can easily integrate your own model:

```python
from spectrumlab.models.base import BaseModel

class CustomModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.model_name = "CustomModel"
        
    def generate(self, prompt, max_out_len=512):
        # Implement the logic for calling your model
        # This could be API calls, local model inference, etc.
        return response
```

**Custom requirements：**

- The `generate` method must be implemented
- Support text and multimodal input
- Return the response in string format

## Evaluator Module

Evaluator This module is responsible for the core logic of model evaluation, providing a standardized evaluation process and flexible customization options.

### Basic usage

For evaluation tasks of the multiple - choice question type, you can directly use `ChoiceEvaluator`:

```python
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator

evaluator = ChoiceEvaluator()

results = evaluator.evaluate(
    data_items=data,
    model=model,
    max_out_len=512,
    save_path="./eval_results"
)
```

**Parameter description：**

- `data_items`: List of evaluation data
- `model`: Model instance
- `max_out_len`: Maximum output length
- `save_path`: Result saving path

### Customize Evaluator

By inheriting from the `BaseEvaluator` class, you can customize the evaluation logic to meet the requirements of specific tasks:

```python
from spectrumlab.evaluator.base import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def _build_prompt(self, item):
        """Build input prompt words"""
        question = item["question"]
        choices = item["choices"]
        return f"Problem：{question}\nOptions：{choices}\nPlease choose the correct answer.："
    
    def _extract_prediction(self, response, item):
        """Extract the prediction results from the model response"""
        import re
        match = re.search(r'\box\{([^}]+)\}', response)
        return match.group(1) if match else ""
    
    def _calculate_accuracy(self, answer, prediction, item):
        """Calculate accuracy"""
        return answer.strip().lower() == prediction.strip().lower()
```

**Core methods:**

- `_build_prompt`: Build model input based on data items
- `_extract_prediction`: Extract predicted answers from the model output
- `_calculate_accuracy`: Judge whether the prediction is correct

## Complete evaluation example

The following is a complete example of the evaluation process, demonstrating the entire process from data loading to result analysis:

```python
from spectrumlab.benchmark.signal_group import SignalGroup
from spectrumlab.models import GPT4oAPI
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator

# 1. Load data
signal_group = SignalGroup("data")
data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])

# 2. Initialize the model and evaluator
model = GPT4oAPI()
evaluator = ChoiceEvaluator()

# 3. Run evaluation
results = evaluator.evaluate(
    data_items=data, 
    model=model, 
    save_path="./evaluation_results"
)

# 4. View the evaluation results
print(f"Evaluation completed! Overall accuracy: {results['metrics']['overall']['accuracy']:.2f}%")

# View detailed results
for subcategory, metrics in results['metrics']['subcategory_metrics'].items():
    print(f"{subcategory}: {metrics['accuracy']:.2f}% ({metrics['correct']}/{metrics['total']})")
```

## Data format

### Input data format

Each data item follows the following format:

```python
{
    "question": "Based on this infrared spectrogram, what is the most likely compound?？",
    "choices": ["benzoic acid, benzaldehyde, benzyl alcohol, phenylacetic acid"],
    "answer": "benzoic acid",
    "image_path": "./data/signal/ir_001.png",  # optional
    "category": "Chemistry",
    "sub_category": "Spectrum Type Classification"
}
```

### Output result format

The evaluation results include detailed performance indicators.：

```python
{
    "metrics": {
        "overall": {
            "accuracy": 85.5,
            "correct": 171,
            "total": 200
        },
        "subcategory_metrics": {
            "Spectrum Type Classification": {
                "accuracy": 90.0,
                "correct": 45,
                "total": 50
            }
        }
    },
    "saved_files": ["result_001.json"],
    "total_items": 200
}
```

## Environment configuration

Before using the API model, you need to configure the corresponding environment variables:

```bash
# OpenAI models
export OPENAI_API_KEY="your_openai_api_key"

# Anthropic model  
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# DeepSeek model
export DEEPSEEK_API_KEY="your_deepseek_api_key"

# Other models...
```

## Quick start

1. **Install dependencies**：`pip install spectrumlab`
2. **Configure API key**：Set the corresponding environment variables
3. **Load data**：Use the Benchmark module to obtain evaluation data
4. **Select a model**：Initialize the pre-trained model or custom model
5. **Run evaluation**：Use Evaluator to perform the evaluation and save the results
