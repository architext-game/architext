/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        console: ['Consolas', 'Courier New', 'monospace'],
      },
      colors: {
        bg: '#2F0A23',
        almost: '#D5BECE',
        soft: '#9E6D8E',
        muted: '#572B49',
      }
    },
  },
  plugins: [],
}

