# API 参考

SpectrumLab 的详细 API 文档。

## 基准测试模块 (Benchmark)

### get_benchmark_group(level)

获取指定级别的基准测试组。

```python
from spectrumlab.benchmark import get_benchmark_group

# 获取感知组
benchmark = get_benchmark_group("perception")

# 获取语义组
benchmark = get_benchmark_group("semantic")

# 获取生成组
benchmark = get_benchmark_group("generation")

# 获取信号组
benchmark = get_benchmark_group("signal")
```

### BaseGroup 类

#### get_data_by_subcategories(subcategories)

根据子类别获取数据。

**参数:**

- `subcategories` (str | List[str] | "all"): 子类别名称或列表

**返回:**

- `List[Dict]`: 数据项列表

```python
# 获取所有子类别数据
data = benchmark.get_data_by_subcategories("all")

# 获取特定子类别数据
data = benchmark.get_data_by_subcategories(["IR_spectroscopy", "Raman_spectroscopy"])

# 获取单个子类别数据
data = benchmark.get_data_by_subcategories("IR_spectroscopy")
```

#### get_available_subcategories()

获取所有可用的子类别。

**返回:**

- `List[str]`: 可用子类别列表

```python
subcategories = benchmark.get_available_subcategories()
print(subcategories)
```

## 评估器模块 (Evaluator)

### get_evaluator(level)

获取指定级别的评估器。

```python
from spectrumlab.evaluator import get_evaluator

evaluator = get_evaluator("perception")
```

### BaseEvaluator 类

#### evaluate(data_items, model, max_out_len=512, batch_size=None, save_path="./eval_results")

运行评估。

**参数:**

- `data_items` (List[Dict]): 数据项列表
- `model`: 模型对象
- `max_out_len` (int): 最大输出长度
- `batch_size` (int, optional): 批大小（暂未实现）
- `save_path` (str): 结果保存路径

**返回:**

- `Dict`: 评估结果

```python
results = evaluator.evaluate(
    data_items=data,
    model=model,
    max_out_len=512,
    save_path="./eval_results"
)
```

### ChoiceEvaluator 类

继承自 BaseEvaluator，专门用于选择题评估。

- 支持多模态输入（图像+文本）
- 使用 `\box{}` 格式提取预测结果
- 基于 MMAR 的字符串匹配算法

## 模型模块 (Models)

### GPT4oAPI 类

OpenAI GPT-4o 模型接口。

```python
from spectrumlab.models import GPT4oAPI

model = GPT4oAPI()
```

**环境变量:**

- `OPENAI_API_KEY`: OpenAI API 密钥

### DeepSeekAPI 类

DeepSeek 模型接口。

```python
from spectrumlab.models import DeepSeekAPI

model = DeepSeekAPI()
```

**环境变量:**

- `DEEPSEEK_API_KEY`: DeepSeek API 密钥

### InternVLAPI 类

InternVL 模型接口。

```python
from spectrumlab.models import InternVLAPI

model = InternVLAPI()
```

**环境变量:**

- `INTERNVL_API_KEY`: InternVL API 密钥

## 工具模块 (Utils)

### 图像处理

#### prepare_images_for_prompt(image_paths)

为提示词准备图像数据。

**参数:**

- `image_paths` (List[str]): 图像路径列表

**返回:**

- `List[Dict]`: 图像数据列表

#### normalize_image_paths(image_paths_field)

规范化图像路径。

**参数:**

- `image_paths_field`: 图像路径字段

**返回:**

- `List[str]`: 规范化后的图像路径列表

## 数据结构

### 数据项格式

每个数据项包含以下字段：

```python
{
    "question": str,           # 问题文本
    "choices": List[str],      # 选项列表
    "answer": str,             # 正确答案
    "image_path": str,         # 图像路径（可选）
    "category": str,           # 类别
    "sub_category": str        # 子类别
}
```

### 评估结果格式

```python
{
    "metrics": {
        "overall": {
            "accuracy": float,      # 整体准确率
            "correct": int,         # 正确答案数
            "total": int,           # 总题目数
            "no_prediction_count": int  # 无预测数
        },
        "category_metrics": {
            "category_name": {
                "accuracy": float,
                "correct": int,
                "total": int
            }
        },
        "subcategory_metrics": {
            "subcategory_name": {
                "accuracy": float,
                "correct": int,
                "total": int
            }
        }
    },
    "saved_files": List[str],   # 保存的文件路径
    "total_items": int          # 总数据项数
}
```

## 自定义扩展

### 自定义评估器

```python
from spectrumlab.evaluator.base import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def _build_prompt(self, item: Dict) -> str:
        """构建提示词"""
        # 自定义逻辑
        pass
    
    def _extract_prediction(self, response: str, item: Dict) -> str:
        """提取预测结果"""
        # 自定义逻辑
        pass
    
    def _calculate_accuracy(self, answer: str, prediction: str, item: Dict) -> bool:
        """计算准确率"""
        # 自定义逻辑
        pass
```

### 自定义模型

```python
from spectrumlab.models.base import BaseModel

class CustomModel(BaseModel):
    def generate(self, prompt, max_out_len=512):
        """生成响应"""
        # 自定义逻辑
        pass
```

## 相关链接

- [教程](/zh/tutorial)
- [基准测试](/zh/benchmark)
