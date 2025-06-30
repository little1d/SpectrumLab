# 快速开始

本指南将帮助您快速上手 Spectral-Hub。

## 系统要求

- Python 3.10 或更高版本
- pip 或 uv 包管理器

## 安装

### 使用 pip 安装

```bash
pip install specbench
```

### 使用 uv 安装

```bash
uv add specbench
```

## 验证安装

安装完成后，您可以验证安装是否成功：

```bash
specbench --version
```

## 基本使用

### 命令行工具

```bash
# 查看所有可用命令
specbench --help

# 运行模型评估
specbench eval --model your-model-name --dataset your-dataset-name

# 列出可用的数据集
specbench list-datasets

# 列出可用的模型
specbench list-models
```

### Python API

```python
import specbench

# 基本用法
print(specbench.hello())

# 加载数据集
dataset = specbench.load_dataset("dataset_name")

# 运行评估
results = specbench.evaluate(
    model="your_model",
    dataset=dataset,
    metrics=["accuracy", "f1_score"]
)

print(results)
```

## 下一步

- 🏠 [返回首页](/zh/)
- 🌐 [English Documentation](/en/)
- 📝 [API 示例](/en/api-examples)
- 🎯 [GitHub 仓库](https://github.com/your-username/spectral-hub)
