import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export const zh = defineConfig({
    title: "Spectral-Hub",
    description: "化学谱学大模型基准测试工具",
    themeConfig: {
        nav: [
            { text: '首页', link: '/' },
            { text: '快速开始', link: '/zh/getting-started' },
            { text: '中文文档', link: '/zh/' },
        ],
        sidebar: {
            '/zh/': [
                {
                    text: '开始',
                    items: [
                        { text: '介绍', link: '/zh/' },
                        { text: '快速开始', link: '/zh/getting-started' },
                    ]
                }
            ]
        },
        footer: {
            message: '基于 MIT 许可发布',
            copyright: 'Copyright © 2024 Spectral-Hub'
        }
    }
})