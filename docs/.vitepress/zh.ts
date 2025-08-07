import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export const zh = defineConfig({
    lang: 'zh-CN',
    title: "SpectrumLab",
    description: "A pioneering unified platform designed to systematize and accelerate deep learning research in spectroscopy.",

    head: [
        ['link', { rel: 'icon', type: 'image/svg+xml', href: './public/logo.svg' }]
        // ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
        // [
        //     'link',
        //     { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }
        // ],
        // [
        //     'link',
        //     { href: 'https://fonts.googleapis.com/css2?family=Roboto&display=swap', rel: 'stylesheet' }
        // ]
    ],

    themeConfig: {
        siteTitle: "SpectrumLab",
        logo: {
            src: '/logo.svg',
        },
        nav: [
            { text: '教程', link: '/zh/tutorial' },
            { text: 'API', link: '/zh/api' },
            { text: '基准测试', link: '/zh/benchmark' },
            { text: '排行榜', link: 'https://huggingface.co/spaces/SpectrumWorld/SpectrumLeaderboard' },
        ],

        sidebar: {
            '/': [
                {
                    text: '开始使用',
                    items: [
                        { text: '介绍', link: '/' },
                        { text: '教程', link: '/zh/tutorial' },
                    ]
                },
                {
                    text: '文档',
                    items: [
                        { text: 'API 参考', link: '/zh/api' },
                        { text: '基准测试', link: '/zh/benchmark' },
                        { text: '排行榜', link: 'https://huggingface.co/spaces/SpectrumWorld/SpectrumLeaderboard' },
                    ]
                }
            ]
        },
        footer: {
            message: '基于 MIT 许可发布',
            copyright: 'Copyright © 2025 SpectrumLab'
        },
        docFooter: {
            prev: '上一页',
            next: '下一页'
        },
        outline: {
            label: '页面导航'
        },
        lastUpdated: {
            text: '最后更新于'
        },
        darkModeSwitchLabel: '主题',
        lightModeSwitchTitle: '切换到浅色模式',
        darkModeSwitchTitle: '切换到深色模式',
    }
})
