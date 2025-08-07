# 基准测试

## Benchmark 概述

SpectrumLab 的 Benchmark 采用分层架构设计，从信号处理到高级语义理解，全面评估模型在光谱学任务上的能力。基准测试包含四个主要层级，每个层级包含多个子任务，适用于不同类型的谱图分析。

## Benchmark 详情

### 1. 信号层（Signal Level）

基础的谱图信号处理和分析，包括以下子任务：

- **谱图类型分类（Spectrum Type Classification）**：识别不同类型的谱图（红外、核磁、拉曼等）。
- **谱图质量评估（Spectrum Quality Assessment）**：识别谱图是否清晰、完整、以及是否存在明显噪声。
- **基础特征提取（Basic Feature Extraction）**：识别谱图中的基线、峰、峰位、峰强等基本特征。
- **杂质峰检测（Impurity Peak Detection）**：识别谱图中的杂质峰和异常信号。

### 2. 感知层（Perception Level）

进一步的谱图视觉理解和模式识别，涵盖：

- **基本化学性质预测（Basic Property Prediction）**：基于谱图特征预测分子离子峰、溶解性、酸碱性等直接关联的性质。
- **元素组成预测（Elemental Compositional Prediction）**：从质谱等中识别元素组成和同位素模式。
- **官能团识别（Functional Group Recognition）**：根据谱图特征（特别是特征峰位）预测分子可能存在的官能团。
- **谱峰归属（Peak Assignment）**：对谱图中的主要峰进行初步的化学归属。

### 3. 语义层（Semantic Level）

深层的谱图语义理解和化学知识推理，包括：

- **多模态谱图融合（Fusing Spectroscopic Modalities）**：结合多种光谱或分子信息进行综合判断。
- **分子结构解析（Molecular Structure Elucidation）**：根据光谱信息，从多个候选项中匹配正确的分子结构。
- **多模态推理/问答（Multimodal Molecular Reasoning）**：基于光谱、文本信息，进行复杂的化学推理问答。

### 4. 生成层（Generation Level）

创造性地生成新化学信息，主要任务有：

- **前向问题（Forward Problems）**：谱图、SMILES 或两者结合，推断分子结构。
- **逆向问题（Inverse Problems）**：分子结构生成谱图、SMILES 等。
- **无条件生成（De Novo Generation）**：根据特定目标（如特定性质的分子、特定靶点的配体）从头生成新颖、多样且合理的分子结构（SMILES、2D图）及/或预测的多模态信息（谱图、性质）。
