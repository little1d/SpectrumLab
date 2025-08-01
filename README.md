# SpectrumLab

<div align="center">
A pioneering unified platform designed to systematize and accelerate deep learning research in spectroscopy.
</div>

## Quick Start

### Environment Setup

We recommend using conda and uv for environment management:

```bash
# Clone the repository
git clone https://github.com/your-org/SpectrumLab.git
cd SpectrumLab

# Create conda environment
conda create -n spectrumlab python=3.10
conda activate spectrumlab

pip install uv
uv pip install -e .
```

### One-Click Evaluation

1. **Switch to evaluation branch**

   ```bash
   git checkout evaluation
   ```

2. **Download benchmark data**

   Benchmark data is hosted on Hugging Face. Please download it from the following link:

   [https://huggingface.co/datasets/SpectrumWorld/spectrumbench_v_1.0](https://huggingface.co/datasets/SpectrumWorld/spectrumbench_v_1.0)

   After downloading, extract the data to the `data` directory in the project root.

3. **Configure model parameters**

   ```bash
   # Copy and edit environment configuration
   cp .env.example .env
   # Configure your API keys in the .env file
   ```

4. **Run evaluation**

   ```bash
   python run_evaluation.py
   
   # Run in background
   nohup python run_evaluation.py > run_eval.log 2>&1 &
   ```

## 🤝 Contributing

We welcome community contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Acknowledgments

- **Experiment Tracking**: [SwanLab](https://github.com/SwanHubX/SwanLab/) for experiment management and visualization
- **Evaluation Framework**: Inspired by [MMAR](https://github.com/ddlBoJack/MMAR)
