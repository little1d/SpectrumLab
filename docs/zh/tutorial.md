# 教程

这里是 SpectrumLab 的详细使用教程。

## 安装

```bash
pip install spectrumlab
```

## 基础概念

SpectrumLab 主要包含以下几个核心组件：

- **Benchmark**: 基准测试数据管理
- **Evaluator**: 评估器，负责模型评估逻辑
- **Models**: 模型接口，支持多种 API 模型
- **Utils**: 工具函数，如图像处理等

## 快速开始

### 1. 数据加载

```python
from spectrumlab.benchmark import get_benchmark_group

# 加载感知组数据
benchmark = get_benchmark_group("perception")

# 获取所有子类别数据
data = benchmark.get_data_by_subcategories("all")

# 获取特定子类别数据
data = benchmark.get_data_by_subcategories(["IR_spectroscopy", "Raman_spectroscopy"])

# 查看可用子类别
print(benchmark.get_available_subcategories())
```

### 2. 模型初始化

```python
from spectrumlab.models import GPT4oAPI, DeepSeekAPI, InternVLAPI

# 初始化 GPT-4o 模型
model = GPT4oAPI()

# 初始化 DeepSeek 模型
model = DeepSeekAPI()

# 初始化 InternVL 模型
model = InternVLAPI()
```

### 3. 运行评估

```python
from spectrumlab.evaluator import get_evaluator

# 获取评估器
evaluator = get_evaluator("perception")

# 运行评估
results = evaluator.evaluate(
    data_items=data,
    model=model,
    max_out_len=512,
    save_path="./eval_results"
)

# 查看结果
print(f"整体准确率: {results['metrics']['overall']['accuracy']:.2f}%")
print(f"正确答案数: {results['metrics']['overall']['correct']}")
print(f"总题目数: {results['metrics']['overall']['total']}")
```

### 4. 查看详细结果

```python
# 查看各类别准确率
for category, metrics in results['metrics']['category_metrics'].items():
    print(f"{category}: {metrics['accuracy']:.2f}% ({metrics['correct']}/{metrics['total']})")

# 查看各子类别准确率
for subcategory, metrics in results['metrics']['subcategory_metrics'].items():
    print(f"{subcategory}: {metrics['accuracy']:.2f}% ({metrics['correct']}/{metrics['total']})")
```

## 命令行使用

SpectrumLab 也提供了命令行工具：

```bash
# 查看版本
spectrumlab --version

# 运行评估（示例）
spectrumlab eval --model gpt4o --dataset perception
```

## 高级使用

### 自定义评估器

```python
from spectrumlab.evaluator.base import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def _build_prompt(self, item):
        # 自定义提示词构建逻辑
        pass
    
    def _extract_prediction(self, response, item):
        # 自定义预测结果提取逻辑
        pass
    
    def _calculate_accuracy(self, answer, prediction, item):
        # 自定义准确率计算逻辑
        pass
```

### 处理多模态数据

```python
# 查看数据项结构
print(data[0].keys())
# 可能包含: question, choices, answer, image_path, category, sub_category

# 图像路径会被自动处理
if data[0]['image_path']:
    print(f"图像路径: {data[0]['image_path']}")
```

## 配置环境变量

为了使用 API 模型，需要配置相应的环境变量：

```bash
# OpenAI GPT-4o
export OPENAI_API_KEY="your_openai_api_key"

# DeepSeek
export DEEPSEEK_API_KEY="your_deepseek_api_key"

# InternVL
export INTERNVL_API_KEY="your_internvl_api_key"
```

## 更多信息

- 查看 [API 文档](/zh/api) 了解详细的接口说明
- 了解 [基准测试](/zh/benchmark) 查看评估指标和数据集详情
