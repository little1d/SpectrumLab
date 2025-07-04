# Tutorial

This is the detailed tutorial for SpectrumLab.

## Installation

```bash
pip install spectrumlab
```

## Core Concepts

SpectrumLab consists of several core components:

- **Benchmark**: Benchmark data management
- **Evaluator**: Evaluators responsible for model evaluation logic
- **Models**: Model interfaces supporting various API models
- **Utils**: Utility functions like image processing

## Quick Start

### 1. Data Loading

```python
from spectrumlab.benchmark import get_benchmark_group

# Load perception group data
benchmark = get_benchmark_group("perception")

# Get all subcategory data
data = benchmark.get_data_by_subcategories("all")

# Get specific subcategory data
data = benchmark.get_data_by_subcategories(["IR_spectroscopy", "Raman_spectroscopy"])

# View available subcategories
print(benchmark.get_available_subcategories())
```

### 2. Model Initialization

```python
from spectrumlab.models import GPT4oAPI, DeepSeekAPI, InternVLAPI

# Initialize GPT-4o model
model = GPT4oAPI()

# Initialize DeepSeek model
model = DeepSeekAPI()

# Initialize InternVL model
model = InternVLAPI()
```

### 3. Running Evaluation

```python
from spectrumlab.evaluator import get_evaluator

# Get evaluator
evaluator = get_evaluator("perception")

# Run evaluation
results = evaluator.evaluate(
    data_items=data,
    model=model,
    max_out_len=512,
    save_path="./eval_results"
)

# View results
print(f"Overall accuracy: {results['metrics']['overall']['accuracy']:.2f}%")
print(f"Correct answers: {results['metrics']['overall']['correct']}")
print(f"Total questions: {results['metrics']['overall']['total']}")
```

### 4. Viewing Detailed Results

```python
# View category-wise accuracy
for category, metrics in results['metrics']['category_metrics'].items():
    print(f"{category}: {metrics['accuracy']:.2f}% ({metrics['correct']}/{metrics['total']})")

# View subcategory-wise accuracy
for subcategory, metrics in results['metrics']['subcategory_metrics'].items():
    print(f"{subcategory}: {metrics['accuracy']:.2f}% ({metrics['correct']}/{metrics['total']})")
```

## Command Line Usage

SpectrumLab also provides command line tools:

```bash
# Check version
spectrumlab --version

# Run evaluation (example)
spectrumlab eval --model gpt4o --dataset perception
```

## Advanced Usage

### Custom Evaluator

```python
from spectrumlab.evaluator.base import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def _build_prompt(self, item):
        # Custom prompt building logic
        pass
    
    def _extract_prediction(self, response, item):
        # Custom prediction extraction logic
        pass
    
    def _calculate_accuracy(self, answer, prediction, item):
        # Custom accuracy calculation logic
        pass
```

### Handling Multimodal Data

```python
# View data item structure
print(data[0].keys())
# May contain: question, choices, answer, image_path, category, sub_category

# Image paths are automatically processed
if data[0]['image_path']:
    print(f"Image path: {data[0]['image_path']}")
```

## Environment Configuration

To use API models, you need to configure the corresponding environment variables:

```bash
# OpenAI GPT-4o
export OPENAI_API_KEY="your_openai_api_key"

# DeepSeek
export DEEPSEEK_API_KEY="your_deepseek_api_key"

# InternVL
export INTERNVL_API_KEY="your_internvl_api_key"
```

## More Information

- Check [API Documentation](/en/api) for detailed interface descriptions
- Learn about [Benchmark](/en/benchmark) to view evaluation metrics and dataset details
