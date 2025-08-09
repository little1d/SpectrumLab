# SpectrumLab

Comprehensive toolkit for spectroscopy deep learning: dataset loading, training, evaluation, inference, and more.

## What is SpectrumLab?

SpectrumLab is a comprehensive toolkit designed for chemical spectroscopy deep learning, providing complete functionality for dataset loading, model training, evaluation, inference, and more.

## Key Features

- 🔬 **Multimodal Evaluation**: Support for image+text multimodal spectroscopy data evaluation
- 🤖 **Model Integration**: Integrated API interfaces for advanced models like GPT-4o, DeepSeek, InternVL
- 📊 **Benchmark Suite**: Standardized evaluation metrics and datasets for various spectroscopy tasks
- 🚀 **Command Line Tool**: Simple CLI interface with batch evaluation and result management
- 🔧 **Extensibility**: Modular design supporting custom evaluators and models

## Quick Start

### Installation

```bash
pip install spectrumlab
```

### Basic Usage

```python
from spectrumlab.benchmark import get_benchmark_group
from spectrumlab.models import GPT4oAPI
from spectrumlab.evaluator import get_evaluator

# Load benchmark data
benchmark = get_benchmark_group("perception")
data = benchmark.get_data_by_subcategories("all")

# Initialize model
model = GPT4oAPI()

# Get evaluator
evaluator = get_evaluator("perception")

# Run evaluation
results = evaluator.evaluate(
    data_items=data,
    model=model,
    save_path="./results"
)

print(f"Overall accuracy: {results['metrics']['overall']['accuracy']:.2f}%")
```

### Command Line Usage

```bash
# Run evaluation
spectrumlab eval --model gpt4o --dataset perception
```

## Supported Models

- **GPT-4o**: OpenAI's multimodal large language model
- **DeepSeek**: DeepSeek's multimodal model
- **InternVL**: Shanghai AI Lab's vision-language model

## Evaluation Task Types

- **Perception Group**: Spectral image understanding and analysis
- **Semantic Group**: Semantic interpretation of spectral data
- **Generation Group**: Spectral-related content generation
- **Signal Group**: Spectral signal processing

## Get Started

- [Tutorial](/en/tutorial) - Learn how to use SpectrumLab
- [API Reference](/en/api) - Detailed API documentation
- [Benchmark](/en/benchmark) - View benchmark results and metrics
