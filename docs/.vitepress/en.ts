import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export const en = defineConfig({
    lang: 'en-US',
    title: "SpectrumLab",
    description: "A pioneering unified platform designed to systematize and accelerate deep learning research in spectroscopy",
    themeConfig: {
        nav: [
            { text: 'Home', link: '/en/' },
            { text: 'Tutorial', link: '/en/tutorial' },
            { text: 'API', link: '/en/api' },
            { text: 'Benchmark', link: '/en/benchmark' },
        ],
        sidebar: {
            '/en/': [
                {
                    text: 'Getting Started',
                    items: [
                        { text: 'Introduction', link: '/en/' },
                        { text: 'Tutorial', link: '/en/tutorial' },
                    ]
                },
                {
                    text: 'Documentation',
                    items: [
                        { text: 'API Reference', link: '/en/api' },
                        { text: 'Benchmark', link: '/en/benchmark' },
                    ]
                }
            ]
        },
        footer: {
            message: 'Released under the MIT License',
            copyright: 'Copyright © 2025 SpectrumLab'
        },

        // 英文版本的组件文本
        docFooter: {
            prev: 'Previous page',
            next: 'Next page'
        },

        outline: {
            label: 'On this page'
        },

        lastUpdated: {
            text: 'Last updated'
        },

        darkModeSwitchLabel: 'Appearance',
        lightModeSwitchTitle: 'Switch to light theme',
        darkModeSwitchTitle: 'Switch to dark theme',
    }
})