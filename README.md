<!-- # SpectrumLab -->

<div align="center">
  <img src="docs/public/spectrumlab.svg" alt="SpectrumLab" width="600"/>
  
  <p><strong>A pioneering unified platform designed to systematize and accelerate deep learning research in spectroscopy.</strong></p>
</div>

## 🚀 Quick Start

### Environment Setup

We recommend using conda and uv for environment management:

```bash
# Clone the repository
git clone https://github.com/little1d/SpectrumLab.git
cd SpectrumLab

# Create conda environment
conda create -n spectrumlab python=3.10
conda activate spectrumlab

pip install uv
uv pip install -e .
```

### Data Setup

Download benchmark data from Hugging Face:

- [SpectrumBench v1.0](https://huggingface.co/datasets/SpectrumWorld/spectrumbench_v_1.0)

Extract the data to the `data` directory in the project root.

### API Keys Configuration

```bash
# Copy and edit environment configuration
cp .env.example .env
# Configure your API keys in the .env file
```

## 💻 Usage

### Python API

```python
from spectrumlab.benchmark import get_benchmark_group
from spectrumlab.models import GPT4o
from spectrumlab.evaluator import get_evaluator

# Load benchmark data
benchmark = get_benchmark_group("perception")
data = benchmark.get_data_by_subcategories("all")

# Initialize model
model = GPT4o()

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

### Command Line Interface

The CLI provides a simple way to run evaluations:

```bash
# Basic evaluation
spectrumlab eval --model gpt4o --level perception

# Specify data path and output directory
spectrumlab eval --model claude --level signal --data-path ./data --output ./my_results

# Evaluate specific subcategories
spectrumlab eval --model deepseek --level semantic --subcategories "IR_spectroscopy" "Raman_spectroscopy"

# Customize output length
spectrumlab eval --model internvl --level generation --max-length 1024

# Get help
spectrumlab eval --help
```

## 🤝 Contributing

We welcome community contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Acknowledgments

- **Experiment Tracking**: [SwanLab](https://github.com/SwanHubX/SwanLab/) for experiment management and visualization
- **Choice Evaluator Framework**: Inspired by [MMAR](https://github.com/ddlBoJack/MMAR)
