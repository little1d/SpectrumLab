# SpectrumLab

## 什么是 SpectrumLab？

SpectrumLab 是一个专为化学光谱学深度学习而设计的综合工具包，提供数据集加载、模型训练、评估、推理等完整功能。

## 主要特性

- 🔬 **多模态评估**: 支持图像+文本的多模态光谱数据评估
- 🤖 **模型集成**: 集成 GPT-4o、DeepSeek、InternVL 等先进模型的 API 接口
- 📊 **基准测试套件**: 标准化的评估指标和数据集，支持多种光谱学任务
- 🚀 **命令行工具**: 简洁的 CLI 界面，支持批量评估和结果管理
- 🔧 **可扩展性**: 模块化设计，支持自定义评估器和模型

## 快速开始

### 安装

```bash
pip install spectrumlab
```

### 基础使用

```python
from spectrumlab.benchmark import get_benchmark_group
from spectrumlab.models import GPT4oAPI
from spectrumlab.evaluator import get_evaluator

# 加载基准测试数据
benchmark = get_benchmark_group("perception")
data = benchmark.get_data_by_subcategories("all")

# 初始化模型
model = GPT4oAPI()

# 获取评估器
evaluator = get_evaluator("perception")

# 运行评估
results = evaluator.evaluate(
    data_items=data,
    model=model,
    save_path="./results"
)

print(f"整体准确率: {results['metrics']['overall']['accuracy']:.2f}%")
```

### 命令行使用

```bash
# 运行评估
spectrumlab eval --model gpt4o --dataset perception
```

## 支持的模型

- **GPT-4o**: OpenAI 的多模态大语言模型
- **DeepSeek**: DeepSeek 的多模态模型
- **InternVL**: 上海 AI 实验室的视觉语言模型

## 评估任务类型

- **感知组 (Perception)**: 光谱图像理解和分析
- **语义组 (Semantic)**: 光谱数据的语义解释
- **生成组 (Generation)**: 光谱相关内容生成
- **信号组 (Signal)**: 光谱信号处理

## 开始使用

- [教程](/zh/tutorial) - 学习如何使用 SpectrumLab
- [API 参考](/zh/api) - 详细的 API 文档
- [基准测试](/zh/benchmark) - 查看基准结果和指标
