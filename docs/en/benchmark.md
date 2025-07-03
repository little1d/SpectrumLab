# Benchmark

Benchmark tests and evaluation metrics for Spectral-Hub.

## Supported Datasets

- **IR Spectra**: Infrared spectroscopy data
- **Raman Spectra**: Raman spectroscopy data  
- **NMR Spectra**: Nuclear magnetic resonance data

## Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 Score

## Benchmark Results

| Model | Dataset | Accuracy |
|-------|---------|----------|
| Transformer | IR Spectra | 95.2% |
| CNN | Raman | 92.8% |
| LSTM | NMR | 89.5% |

## Running Benchmarks

```python
import spectral_hub as sh

# Run benchmark
results = sh.run_benchmark('all')
print(results)
```

## Related Links

- [Tutorial](/en/tutorial)
- [API Reference](/en/api)
