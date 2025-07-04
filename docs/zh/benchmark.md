# 基准测试

SpectrumLab 的基准测试系统详细介绍。

## 概述

SpectrumLab 提供了一个综合的基准测试框架，用于评估大语言模型在化学光谱学任务上的性能。该框架支持多模态数据（图像+文本）和标准化的评估指标。

## 任务类型

### 感知组 (Perception)

**任务描述:** 光谱图像理解和分析

**特点:**

- 多模态输入（光谱图像 + 文本问题）
- 选择题格式
- 涵盖多种光谱类型（红外、拉曼、核磁等）

**使用示例:**

```python
from spectrumlab.benchmark import get_benchmark_group

benchmark = get_benchmark_group("perception")
data = benchmark.get_data_by_subcategories("all")
```

### 语义组 (Semantic)

**任务描述:** 光谱数据的语义解释

**特点:**

- 专注于光谱数据的语义理解
- 化学结构与光谱特征的对应关系
- 光谱解释的准确性评估

### 生成组 (Generation)

**任务描述:** 光谱相关内容生成

**特点:**

- 基于光谱数据生成描述性内容
- 光谱分析报告生成
- 化学结构预测

### 信号组 (Signal)

**任务描述:** 光谱信号处理

**特点:**

- 光谱信号的预处理和分析
- 峰值识别和特征提取
- 信号质量评估

## 数据结构

### 数据项格式

每个数据项包含以下字段：

```python
{
    "question": "关于该红外光谱图，以下哪个化合物最可能对应该谱图？",
    "choices": [
        "苯甲酸",
        "苯甲醛", 
        "苯甲醇",
        "苯乙酸"
    ],
    "answer": "苯甲酸",
    "image_path": "./data/perception/IR_spectroscopy/image_001.png",
    "category": "Chemistry",
    "sub_category": "IR_spectroscopy"
}
```

### 字段说明

- `question`: 问题文本
- `choices`: 选项列表（多选题）
- `answer`: 正确答案
- `image_path`: 光谱图像路径（如果有）
- `category`: 主类别
- `sub_category`: 子类别

## 评估指标

### 准确率 (Accuracy)

主要评估指标，计算公式：

```
准确率 = 正确答案数 / 总题目数 × 100%
```

### 分类统计

- **整体准确率**: 所有题目的总体准确率
- **类别准确率**: 按主类别分组的准确率
- **子类别准确率**: 按子类别分组的准确率

### 评估算法

使用基于 MMAR 的字符串匹配算法：

1. **文本标记化**: 将答案和预测结果分解为单词标记
2. **正确匹配**: 检查预测结果是否包含正确答案的所有标记
3. **错误排除**: 确保预测结果不包含错误选项的标记

## 使用流程

### 1. 加载数据

```python
from spectrumlab.benchmark import get_benchmark_group

# 加载特定任务组
benchmark = get_benchmark_group("perception")

# 查看可用子类别
print(benchmark.get_available_subcategories())

# 加载数据
data = benchmark.get_data_by_subcategories("all")
```

### 2. 初始化模型

```python
from spectrumlab.models import GPT4oAPI

model = GPT4oAPI()
```

### 3. 运行评估

```python
from spectrumlab.evaluator import get_evaluator

evaluator = get_evaluator("perception")
results = evaluator.evaluate(
    data_items=data,
    model=model,
    save_path="./results"
)
```

### 4. 查看结果

```python
# 整体结果
print(f"整体准确率: {results['metrics']['overall']['accuracy']:.2f}%")

# 分类结果
for category, metrics in results['metrics']['category_metrics'].items():
    print(f"{category}: {metrics['accuracy']:.2f}%")

# 子类别结果
for subcategory, metrics in results['metrics']['subcategory_metrics'].items():
    print(f"{subcategory}: {metrics['accuracy']:.2f}%")
```

## 结果保存

评估结果会自动保存为 JSON 格式，按子类别分组：

```
./results/
├── IR_spectroscopy_20240101_120000.json
├── Raman_spectroscopy_20240101_120000.json
└── NMR_spectroscopy_20240101_120000.json
```

每个文件包含：

- 原始数据项
- 模型预测结果
- 模型完整响应
- 评估结果（正确/错误）

## 数据集管理

### 本地数据集

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

### 远程数据集

支持从 HuggingFace 加载数据集（待实现）。

## 扩展功能

### 自定义评估器

```python
from spectrumlab.evaluator.base import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def _build_prompt(self, item):
        # 自定义提示词构建
        pass
    
    def _extract_prediction(self, response, item):
        # 自定义预测结果提取
        pass
    
    def _calculate_accuracy(self, answer, prediction, item):
        # 自定义准确率计算
        pass
```

### 自定义数据集

按照标准格式准备数据：

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

## 最佳实践

1. **环境变量配置**: 确保正确设置模型 API 密钥
2. **数据路径检查**: 验证图像文件路径的正确性
3. **结果分析**: 详细分析各子类别的性能表现
4. **批量评估**: 使用脚本进行大规模评估
5. **结果备份**: 定期备份评估结果文件

## 相关链接

- [教程](/zh/tutorial)
- [API 参考](/zh/api)
