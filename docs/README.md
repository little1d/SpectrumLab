# SpectrumLab Documentation

Welcome to the SpectrumLab documentation! This guide will help you contribute to our documentation system.

## About This Documentation

This documentation is built with [VitePress](https://vitepress.dev/), a static site generator designed for creating fast, beautiful documentation websites. Our documentation supports both English and Chinese languages to serve our global community.

## Contributing to the Documentation

Contributing to our documentation is straightforward! Simply clone the project, add or modify Markdown files, commit your changes, and create a Pull Request.

### Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/) (version 18 or higher)
- [npm](https://www.npmjs.com/) (comes with Node.js)

### Step 1: Clone the Repository

```bash
git clone https://github.com/little1d/SpectrumLab.git
cd SpectrumLab
```

### Step 2: Install Dependencies

Navigate to the docs directory and install the required dependencies:

```bash
cd docs
npm install
```

Alternatively, if you prefer using the development dependencies globally:

```bash
npm add -D vitepress
npm install
```

### Step 3: Create a New Branch

Create a new branch for your documentation changes. We recommend using the naming convention `docs/<section-name>` (e.g., `docs/api`, `docs/examples`, `docs/benchmarks`).

```bash
git checkout -b docs/<your-section-name>
```

For detailed branching and contribution guidelines, please refer to our [CONTRIBUTING.md](../CONTRIBUTING.md).

### Step 4: Preview Your Changes

#### Local Development

To start the development server and preview your changes in real-time:

```bash
npm run docs:dev
```

This will start a local server (typically at `http://localhost:5173`) where you can preview your documentation changes.

#### Production Build

If you need to test the complete compilation and packaging:

```bash
# Build the documentation
npm run docs:build

# Preview the production build
npm run docs:preview
```

> **Note:** These commands are configured in `docs/package.json`. You can modify them if needed.

### Step 5: Deployment

We have automated deployment set up using [GitHub Actions](.github/workflows/docs-deploy.yml). The deployment process is triggered automatically when:

- Changes are pushed to the `main` branch
- Changes are made to files in the `docs/` directory
- Changes are made to the deployment workflow file

**All you need to do is create a Pull Request!** Once your PR is merged into the main branch, the documentation will be automatically deployed to GitHub Pages.

## Documentation Structure

Our documentation is organized as follows:

```
docs/
├── .vitepress/          # VitePress configuration
├── public/              # Static assets
├── assets/              # Documentation assets
├── en/                  # English documentation
│   ├── index.md
│   ├── tutorial.md
│   ├── api.md
│   └── benchmark.md
├── zh/                  # Chinese documentation
│   ├── index.md
│   ├── tutorial.md
│   ├── api.md
│   └── benchmark.md
├── index.md             # Homepage
├── package.json         # Dependencies and scripts
└── README.md           # This file
```

## Writing Guidelines

### Language Support

- **English**: Primary language for the documentation
- **Chinese**: Full translation available for Chinese-speaking users

### Content Guidelines

1. **Be Clear and Concise**: Write in simple, clear language
2. **Use Code Examples**: Include practical examples wherever possible
3. **Maintain Consistency**: Follow the existing style and structure
4. **Cross-Reference**: Link to related sections when appropriate

### Markdown Features

VitePress supports many Markdown features including:

- **Code Blocks**: With syntax highlighting
- **Custom Containers**: For tips, warnings, and notes
- **Mathematical Expressions**: Using LaTeX syntax
- **Mermaid Diagrams**: For flowcharts and diagrams

Example:

```markdown
::: tip
This is a helpful tip!
:::

::: warning
This is a warning message.
:::

::: danger
This is a danger alert.
:::
```

## Getting Help

If you encounter any issues or have questions about contributing to the documentation:

1. Check our [existing issues](https://github.com/little1d/SpectrumLab/issues)
2. Create a new issue with the `documentation` label
3. Refer to the [VitePress documentation](https://vitepress.dev/) for technical questions
4. Review our [CONTRIBUTING.md](../CONTRIBUTING.md) for general contribution guidelines

## Resources

- [VitePress Guide](https://vitepress.dev/guide/getting-started)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Docs: About Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)

Thank you for contributing to SpectrumLab documentation! 🎉
