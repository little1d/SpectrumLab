# 如何为本项目做出贡献

## 标准开发流程

1. 浏览 Github 上的 Issues ，查看你愿意添加的功能或修复的错误，以及它们是否被 Pull Request
   - 如果没有，请创建一个新 Issues，除非您的 PR 非常小，否则 PR 应该指向具体的 Issues，这样可以避免重复重做，同时提高代码审查效率。
2. 如果你是第一次为项目贡献代码，请转到仓库首页单击右上角的"Fork"按钮，这将创建你用于开发的仓库副本

   - 将 Fork 的项目克隆到你的计算机，并添加指向本项目的远程链接：

   ```bash
   git clone https://github.com/<your-username>/hello.git
   cd hello
   git remote add upstream https://github.com/hello.git
   ```

3. 开发你的贡献

   - 确保您的 Fork 与主存储库同步：

   ```bash
   git checkout main
   git pull upstream main
   ```

   - 创建一个 `git`分支，您将在其中开发您的贡献。为分支使用合理的名称，例如：

   ```bash
   git checkout -b <username>/<short-dash-seperated-feature-description>
   ```

   - 当你取得进展时，在本地提交你的改动，例如：

   ```bash
   git add changed-file.py test/test-changed-file.py
   git commit -m "feat(integreations): Add integration with the `awosome` library"
   ```

4. 发起贡献:

   - [Github Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
   - 当您的贡献准备就绪后，将您的分支推送到 Github:

   ```bash
   git push origin <username>/<short-dash-seperated-feature-description>
   ```

   - 分支上传后，`Github` 将打印一个 URL，用于将您的贡献作为拉取请求提交。在浏览器中打开该 URL，为您的拉取请求编写信息丰富的标题和详细描述，然后提交。

   - 请将相关 Issue（现有 Issue 或您创建的 Issue）链接到您的 PR。请参阅 PR 页面的右栏。或者，在 PR
     描述中提及“修复问题链接” - GitHub 将自动进行链接。

   - 我们将审查您的贡献并提供反馈。要合并审阅者建议的更改，请将编辑提交到您的分支，然后再次推送到分支（无需重新创建拉取请求，它将自动跟踪对分支的修改），例如：

   ```bash
   git add tests/test-changed-file.py
   git commit -m "test(sdk): Add a test case to address reviewer feedback"
   git push origin <username>/<short-dash-seperated-feature-description>
   ```

   - 一旦您的拉取请求被审阅者批准，它将被合并到存储库的主分支中。

## 安装环境

打开您所使用的 python 环境，在根目录下执行以下命令

```bash
pip install uv

uv pip install -e .
```
