import { defineConfig } from 'vitepress'
import { en } from './en'
import { zh } from './zh'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: '/spectral-hub/',
  themeConfig: {
    lastUpdated: {
      text: "Updated at",
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'medium',
      },
    },
  },
  markdown: {
    image: {
      lazyLoading: true,
    },
  },

  locales: {
    root: { label: '简体中文', ...zh },
    en: { label: 'English', ...en },
  },
})
