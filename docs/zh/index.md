# Spectral-Hub

化学谱学大模型基准测试工具

## 什么是 Spectral-Hub？

Spectral-Hub 是一个专为化学光谱学基准测试和模型评估而设计的综合工具包。

## 主要特性

- 🔬 **多种光谱类型**: 支持红外、拉曼、核磁共振光谱
- 🤖 **预训练模型**: 针对各种光谱分析任务的即用型模型
- 📊 **基准测试套件**: 标准化的评估指标和数据集
- 🚀 **易于使用**: 简单的 API，便于快速集成

## 快速开始

```python
import spectral_hub as sh

# 加载数据集
data = sh.load_dataset('ir_spectra')

# 创建并训练模型
model = sh.SpectralModel()
model.train(data)

# 评估性能
results = model.evaluate()
```

## 开始使用

- [教程](/zh/tutorial) - 学习如何使用 Spectral-Hub
- [API 参考](/zh/api) - 详细的 API 文档
- [基准测试](/zh/benchmark) - 查看基准结果和指标
