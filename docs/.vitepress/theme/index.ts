import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
    extends: DefaultTheme,
    enhanceApp({ app, router, siteData }) {
        // 注册全局组件
        // app.component('MyGlobalComponent', MyGlobalComponent)

        // 全局属性
        // app.config.globalProperties.$myGlobalProperty = () => {}
    }
} satisfies Theme