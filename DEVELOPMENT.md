# Development Guide

## 解决模块导入问题

如果你遇到 `ModuleNotFoundError: No module named 'spectrumlab'` 错误，请按照以下步骤解决：

### 方法1: 安装开发模式（推荐）

```bash
# 在项目根目录运行
pip install -e .
```

### 方法2: 使用安装脚本

```bash
# 在项目根目录运行
python install_dev.py
```

### 方法3: 手动设置Python路径

```bash
# 在项目根目录运行测试
PYTHONPATH=. python -m pytest tests/
```

或者在Python脚本中：

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

## 运行测试

安装完成后，你可以运行测试：

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/models/test_claude.py

# 运行导入测试
python -m pytest tests/test_import.py
```

## 环境配置

确保你已经在项目根目录创建了 `.env` 文件，包含必要的API密钥：

```env
# Claude API Configuration
CLAUDE_API_KEY=your_claude_key
CLAUDE_BASE_URL=https://api.claude.com
CLAUDE_MODEL_NAME=claude-model

# 其他API配置...
```

## 常见问题

### 1. 导入错误
- 确保在项目根目录运行命令
- 确保已安装所有依赖：`pip install -r requirements.txt`
- 尝试重新安装开发模式：`pip install -e . --force-reinstall`

### 2. 环境变量问题
- 确保 `.env` 文件在项目根目录
- 检查环境变量是否正确设置
- 重启Python解释器或IDE

### 3. 测试失败
- 检查API密钥是否正确配置
- 确保网络连接正常
- 查看具体的错误信息 