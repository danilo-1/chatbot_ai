

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap/dist/js/bootstrap.bundle.js' 
import { marked } from 'marked'
import hljs from 'highlight.js'               // npm i highlight.js
import 'highlight.js/styles/github-dark.css'  // tema pronto – troque à vontade
import piniaPersist from 'pinia-plugin-persistedstate'

import { useTheme } from './composables/useTheme';

const { theme, toggle } = useTheme()
theme.value = localStorage.getItem('theme') || 'light'
document.documentElement.setAttribute('data-bs-theme', theme.value)

marked.setOptions({
  highlight (code, lang) {
    // se vier a linguagem no fence (```ts, ```js …) usa; senão detecta
    const valid = lang && hljs.getLanguage(lang)
    return valid
      ? hljs.highlight(code, { language: lang }).value
      : hljs.highlightAuto(code).value
  }
})

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPersist)
app.use(pinia)
app.use(router)

app.mount('#app')