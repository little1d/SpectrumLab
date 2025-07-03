# 基准测试

Spectral-Hub 的基准测试和评估指标。

## 支持的数据集

- **IR Spectra**: 红外光谱数据
- **Raman Spectra**: 拉曼光谱数据  
- **NMR Spectra**: 核磁共振数据

## 评估指标

- 准确率 (Accuracy)
- 精确率 (Precision)
- 召回率 (Recall)
- F1 分数

## 基准结果

| 模型 | 数据集 | 准确率 |
|------|--------|---------|
| Transformer | IR Spectra | 95.2% |
| CNN | Raman | 92.8% |
| LSTM | NMR | 89.5% |

## 运行基准测试

```python
import spectral_hub as sh

# 运行基准测试
results = sh.run_benchmark('all')
print(results)
```

## 相关链接

- [教程](/zh/tutorial)
- [API 参考](/zh/api)
