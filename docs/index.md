---
layout: home

hero:
  name: "SpectrumLab"
  text: ""
  tagline: "一个为系统评估和加速谱学深度学习的平台"
  actions:
    - theme: brand
      text: 快速开始
      link: /tutorial
    - theme: alt
      text: 查看源码
      link: https://github.com/little1d/SpectrumLab

features:
  - title: 🔬 多模态评估
    details: 支持图像+文本的多模态光谱数据评估，兼容多种深度学习模型
  - title: 🤖 模型集成
    details: 集成 GPT-4o、Claude、DeepSeek、Qwen-VL 等先进模型的 API 接口
  - title: 📊 基准测试
    details: 提供标准化的评估流程和指标，支持多种光谱学任务类型
  - title: 🏆 排行榜
    details: 实时更新的模型性能排行榜，支持多维度对比分析
  - title: 🚀 命令行工具
    details: 简洁的命令行界面，支持批量评估和结果管理
  - title: 🔧 易于扩展
    details: 模块化设计，支持自定义评估器和模型的快速集成
---

## 什么是 SpectrumLab？

SpectrumLab 是一个专为光谱学深度学习设计的综合性多模态基准测试平台。它旨在推动光谱学领域的人工智能研究和应用，为研究人员和开发者提供标准化的评估工具和流程。

### 🎯 核心特性

- **四层评估体系**：Signal、Perception、Semantic、Generation 四个层级
- **丰富任务类型**：分类、预测、识别、生成等多种任务
- **多模态支持**：图像、文本等多种输入格式
- **标准化评估**：统一的评估指标和流程

### 🏗️ 支持的模型

- **OpenAI**: GPT-4V, GPT-4o, GPT-4.1
- **Anthropic**: Claude 3.5 Sonnet, Claude 3.5 Haiku
- **DeepSeek**: DeepSeek-VL
- **Qwen**: Qwen-VL, Qwen2.5-VL
- **InternLM**: InternVL
- **字节跳动**: Doubao-VL
- **Meta**: Llama 3.2 Vision
- **xAI**: Grok-Vision

### 📈 评估任务

- **Signal Level**: 光谱类型分类、特征提取、质量评估
- **Perception Level**: 官能团识别、峰位归属、性质预测  
- **Semantic Level**: 分子结构理解、化学反应分析
- **Generation Level**: 光谱解释生成、实验建议

## 快速开始

```bash
# 克隆项目
git clone https://github.com/your-org/SpectrumLab.git
cd SpectrumLab

# 安装环境
conda create -n spectrumlab python=3.10
conda activate spectrumlab
pip install uv
uv pip install -e .

# 运行评估
python run_evaluation.py
```

## 开始使用

- [教程](/tutorial) - 学习如何使用 SpectrumLab
- [API 参考](/api) - 详细的 API 文档  
- [基准测试](/benchmark) - 查看基准结果和指标
- [排行榜](/leaderboard) - 模型性能排行榜
