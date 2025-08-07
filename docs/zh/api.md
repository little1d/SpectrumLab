# API Reference

SpectrumLab 提供了简洁而强大的 API 接口，帮助你快速构建光谱学深度学习应用。本文档涵盖了核心模块的使用方法和自定义扩展指南。

## Benchmark 模块

Benchmark 模块是 SpectrumLab 的数据访问核心，提供了统一的接口来加载和管理不同层级的光谱学基准测试数据。

### 获取 Benchmark Group

通过 `get_benchmark_group` 函数可以获取四个不同层级的基准测试组：

```python
from spectrumlab.benchmark import get_benchmark_group

signal_group = get_benchmark_group("signal")        # 信号层
perception_group = get_benchmark_group("perception")  # 感知层
semantic_group = get_benchmark_group("semantic")      # 语义层
generation_group = get_benchmark_group("generation")  # 生成层
```

### 数据访问

每个 Benchmark Group 提供了灵活的数据访问方法：

```python
# 获取所有数据
data = signal_group.get_data_by_subcategories("all")

# 获取特定子类别数据
data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])

# 获取 Benchmark Group 可用的所有 sub-categories
subcategories = signal_group.get_available_subcategories()
print(subcategories)
```

**方法说明：**

- `get_data_by_subcategories("all")`: 返回该层级下所有子类别的数据
- `get_data_by_subcategories([...])`: 返回指定子类别的数据列表
- `get_available_subcategories()`: 查看当前层级包含的所有子类别名称

## Model 模块

Model 模块提供了统一的模型接口，支持多种预训练模型和自定义模型的集成。

### 使用现有模型

SpectrumLab 内置了多种先进的多模态模型接口：

```python
from spectrumlab.models import GPT4oAPI

gpt4o = GPT4oAPI()

response = gpt4o.generate("Your Prompts")
```

**支持的模型：**

- `GPT4oAPI`: OpenAI GPT-4o
- `ClaudeAPI`: Anthropic Claude 系列
- `DeepSeekAPI`: DeepSeek-VL
- `QwenVLAPI`: Qwen-VL 系列
- `InternVLAPI`: InternVL 系列

### 自定义模型

通过继承 `BaseModel` 类，你可以轻松集成自己的模型：

```python
from spectrumlab.models.base import BaseModel

class CustomModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.model_name = "CustomModel"
        
    def generate(self, prompt, max_out_len=512):
        # 实现你的模型调用逻辑
        # 这里可以是 API 调用、本地模型推理等
        return response
```

**自定义要求：**

- 必须实现 `generate` 方法
- 支持文本和多模态输入
- 返回字符串格式的响应

## Evaluator 模块

Evaluator 模块负责模型评估的核心逻辑，提供了标准化的评估流程和灵活的自定义选项。

### 基础使用

对于选择题类型的评估任务，可以直接使用 `ChoiceEvaluator`：

```python
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator

evaluator = ChoiceEvaluator()

results = evaluator.evaluate(
    data_items=data,
    model=model,
    max_out_len=512,
    save_path="./eval_results"
)
```

**参数说明：**

- `data_items`: 评估数据列表
- `model`: 模型实例
- `max_out_len`: 最大输出长度
- `save_path`: 结果保存路径

### 自定义 Evaluator

通过继承 `BaseEvaluator` 类，你可以定制评估逻辑以适应特定任务需求：

```python
from spectrumlab.evaluator.base import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def _build_prompt(self, item):
        """构建输入提示词"""
        question = item["question"]
        choices = item["choices"]
        return f"问题：{question}\n选项：{choices}\n请选择正确答案："
    
    def _extract_prediction(self, response, item):
        """从模型响应中提取预测结果"""
        import re
        match = re.search(r'\box\{([^}]+)\}', response)
        return match.group(1) if match else ""
    
    def _calculate_accuracy(self, answer, prediction, item):
        """计算准确率"""
        return answer.strip().lower() == prediction.strip().lower()
```

**核心方法：**

- `_build_prompt`: 根据数据项构建模型输入
- `_extract_prediction`: 从模型输出中提取预测答案
- `_calculate_accuracy`: 判断预测是否正确

## 完整评估示例

以下是一个完整的评估流程示例，展示了从数据加载到结果分析的全过程：

```python
from spectrumlab.benchmark.signal_group import SignalGroup
from spectrumlab.models import GPT4oAPI
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator

# 1. 加载数据
signal_group = SignalGroup("data")
data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])

# 2. 初始化模型和评估器
model = GPT4oAPI()
evaluator = ChoiceEvaluator()

# 3. 运行评估
results = evaluator.evaluate(
    data_items=data, 
    model=model, 
    save_path="./evaluation_results"
)

# 4. 查看评估结果
print(f"评估完成！整体准确率: {results['metrics']['overall']['accuracy']:.2f}%")

# 查看详细结果
for subcategory, metrics in results['metrics']['subcategory_metrics'].items():
    print(f"{subcategory}: {metrics['accuracy']:.2f}% ({metrics['correct']}/{metrics['total']})")
```

## 数据格式

### 输入数据格式

每个数据项遵循以下格式：

```python
{
    "question": "基于该红外光谱图，该化合物最可能是？",
    "choices": ["苯甲酸", "苯甲醛", "苯甲醇", "苯乙酸"],
    "answer": "苯甲酸",
    "image_path": "./data/signal/ir_001.png",  # 可选
    "category": "Chemistry",
    "sub_category": "Spectrum Type Classification"
}
```

### 输出结果格式

评估结果包含详细的性能指标：

```python
{
    "metrics": {
        "overall": {
            "accuracy": 85.5,
            "correct": 171,
            "total": 200
        },
        "subcategory_metrics": {
            "Spectrum Type Classification": {
                "accuracy": 90.0,
                "correct": 45,
                "total": 50
            }
        }
    },
    "saved_files": ["result_001.json"],
    "total_items": 200
}
```

## 环境配置

使用 API 模型前需要配置相应的环境变量：

```bash
# OpenAI 模型
export OPENAI_API_KEY="your_openai_api_key"

# Anthropic 模型  
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# DeepSeek 模型
export DEEPSEEK_API_KEY="your_deepseek_api_key"

# 其他模型...
```

## 快速开始

1. **安装依赖**：`pip install spectrumlab`
2. **配置 API 密钥**：设置相应的环境变量
3. **加载数据**：使用 Benchmark 模块获取评估数据
4. **选择模型**：初始化预训练模型或自定义模型
5. **运行评估**：使用 Evaluator 执行评估并保存结果
