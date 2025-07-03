# 教程

这里是 Spectral-Hub 的使用教程。

## 安装

```bash
pip install spectral-hub
```

## 基础使用

```python
import spectral_hub as sh

# 加载数据
data = sh.load_dataset('example')

# 创建模型
model = sh.create_model()

# 训练
model.train(data)
```

## 更多信息

- 查看 [API 文档](/zh/api)
- 了解 [基准测试](/zh/benchmark)
