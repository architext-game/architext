import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({command, mode}) => {
  return {
    plugins: [react()],
    base: process.env.VITE_BASE_PATH ?? '/',
  }
})
