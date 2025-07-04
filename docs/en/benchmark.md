# Benchmark

Detailed introduction to SpectrumLab's benchmark system.

## Overview

SpectrumLab provides a comprehensive benchmark framework for evaluating large language models' performance on chemical spectroscopy tasks. The framework supports multimodal data (image + text) and standardized evaluation metrics.

## Task Types

### Perception Group

**Task Description:** Spectral image understanding and analysis

**Features:**

- Multimodal input (spectral images + text questions)
- Multiple choice format
- Covers various spectral types (IR, Raman, NMR, etc.)

**Usage Example:**

```python
from spectrumlab.benchmark import get_benchmark_group

benchmark = get_benchmark_group("perception")
data = benchmark.get_data_by_subcategories("all")
```

### Semantic Group

**Task Description:** Semantic interpretation of spectral data

**Features:**

- Focus on semantic understanding of spectral data
- Correspondence between chemical structures and spectral features
- Accuracy evaluation of spectral interpretation

### Generation Group

**Task Description:** Spectral-related content generation

**Features:**

- Generate descriptive content based on spectral data
- Spectral analysis report generation
- Chemical structure prediction

### Signal Group

**Task Description:** Spectral signal processing

**Features:**

- Preprocessing and analysis of spectral signals
- Peak identification and feature extraction
- Signal quality assessment

## Data Structure

### Data Item Format

Each data item contains the following fields:

```python
{
    "question": "Regarding this IR spectrum, which compound most likely corresponds to this spectrum?",
    "choices": [
        "Benzoic acid",
        "Benzaldehyde", 
        "Benzyl alcohol",
        "Phenylacetic acid"
    ],
    "answer": "Benzoic acid",
    "image_path": "./data/perception/IR_spectroscopy/image_001.png",
    "category": "Chemistry",
    "sub_category": "IR_spectroscopy"
}
```

### Field Descriptions

- `question`: Question text
- `choices`: List of choices (multiple choice)
- `answer`: Correct answer
- `image_path`: Path to spectral image (if available)
- `category`: Main category
- `sub_category`: Subcategory

## Evaluation Metrics

### Accuracy

Main evaluation metric, calculated as:

```
Accuracy = Number of Correct Answers / Total Number of Questions × 100%
```

### Classification Statistics

- **Overall Accuracy**: Total accuracy across all questions
- **Category Accuracy**: Accuracy grouped by main category
- **Subcategory Accuracy**: Accuracy grouped by subcategory

### Evaluation Algorithm

Uses MMAR-based string matching algorithm:

1. **Text Tokenization**: Decompose answers and predictions into word tokens
2. **Correct Matching**: Check if prediction contains all tokens from correct answer
3. **Error Exclusion**: Ensure prediction doesn't contain tokens from incorrect choices

## Usage Workflow

### 1. Load Data

```python
from spectrumlab.benchmark import get_benchmark_group

# Load specific task group
benchmark = get_benchmark_group("perception")

# View available subcategories
print(benchmark.get_available_subcategories())

# Load data
data = benchmark.get_data_by_subcategories("all")
```

### 2. Initialize Model

```python
from spectrumlab.models import GPT4oAPI

model = GPT4oAPI()
```

### 3. Run Evaluation

```python
from spectrumlab.evaluator import get_evaluator

evaluator = get_evaluator("perception")
results = evaluator.evaluate(
    data_items=data,
    model=model,
    save_path="./results"
)
```

### 4. View Results

```python
# Overall results
print(f"Overall accuracy: {results['metrics']['overall']['accuracy']:.2f}%")

# Category results
for category, metrics in results['metrics']['category_metrics'].items():
    print(f"{category}: {metrics['accuracy']:.2f}%")

# Subcategory results
for subcategory, metrics in results['metrics']['subcategory_metrics'].items():
    print(f"{subcategory}: {metrics['accuracy']:.2f}%")
```

## Result Saving

Evaluation results are automatically saved in JSON format, grouped by subcategory:

```
./results/
├── IR_spectroscopy_20240101_120000.json
├── Raman_spectroscopy_20240101_120000.json
└── NMR_spectroscopy_20240101_120000.json
```

Each file contains:

- Original data items
- Model predictions
- Complete model responses
- Evaluation results (correct/incorrect)

## Dataset Management

### Local Datasets

```
./data/
├── perception/
│   ├── IR_spectroscopy/
│   │   ├── IR_spectroscopy_datasets.json
│   │   └── images/
│   ├── Raman_spectroscopy/
│   │   ├── Raman_spectroscopy_datasets.json
│   │   └── images/
│   └── ...
├── semantic/
├── generation/
└── signal/
```

### Remote Datasets

Support for loading datasets from HuggingFace (to be implemented).

## Extensions

### Custom Evaluator

```python
from spectrumlab.evaluator.base import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def _build_prompt(self, item):
        # Custom prompt building
        pass
    
    def _extract_prediction(self, response, item):
        # Custom prediction extraction
        pass
    
    def _calculate_accuracy(self, answer, prediction, item):
        # Custom accuracy calculation
        pass
```

### Custom Dataset

Prepare data in standard format:

```python
[
    {
        "question": "your question",
        "choices": ["A", "B", "C", "D"],
        "answer": "A",
        "image_path": "path/to/image.png",
        "category": "Chemistry",
        "sub_category": "Custom_Category"
    }
]
```

## Best Practices

1. **Environment Configuration**: Ensure correct model API key setup
2. **Data Path Verification**: Verify correctness of image file paths
3. **Result Analysis**: Detailed analysis of performance across subcategories
4. **Batch Evaluation**: Use scripts for large-scale evaluation
5. **Result Backup**: Regularly backup evaluation result files
