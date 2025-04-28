// composables/useTheme.ts
import { ref, watch } from 'vue'

const theme = ref(localStorage.getItem('theme') || 'light')

watch(theme, val => localStorage.setItem('theme', val))

export const useTheme = () => ({
  theme,
  toggle () {
    console.log('toggle')
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    console.log('theme.value', theme.value)
    document.documentElement.setAttribute('data-bs-theme', theme.value)
    localStorage.setItem('theme', theme.value)
  }
})
