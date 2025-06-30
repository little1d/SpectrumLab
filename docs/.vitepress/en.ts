import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export const en = defineConfig({
    title: "Spectral-Hub",
    description: "An Excellent Toolkit for Spectral Benchmark.",
    lang: 'en-US',
    themeConfig: {
        nav: [
            { text: 'Home', link: '/en/' },
            { text: 'Quick Start', link: '/en/quick-start' },
            { text: 'API', link: '/en/api-examples' },
        ],
        sidebar: {
            '/en/': [
                {
                    text: 'Getting Started',
                    items: [
                        { text: 'Introduction', link: '/en/' },
                        { text: 'Quick Start', link: '/en/quick-start' },
                    ]
                },
                {
                    text: 'Examples',
                    items: [
                        { text: 'API Examples', link: '/en/api-examples' },
                        { text: 'Markdown Examples', link: '/en/markdown-examples' },
                    ]
                }
            ]
        },
        footer: {
            message: 'Released under the MIT License',
            copyright: 'Copyright © 2024 Spectral-Hub'
        }
    }
})