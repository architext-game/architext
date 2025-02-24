import type { Config } from "tailwindcss";


export const colors = {
  background: '#2F0A23',
  highlightBackground: '#3F1B3A',
  foreground: '#171717',
  text: '#FFFFFF',
}

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        backgroundHighlight: "var(--background-highlight)",
        foreground: "var(--foreground)",
        text: "var(--text)",

        // Used by the old code that should be refactored
        bg: '#2F0A23',
        almost: '#D5BECE',
        soft: '#9E6D8E',
        muted: '#572B49',
      },
      fontFamily: {
        mono: ['mononoki-Regular', 'monospace'],
      },
    },
  },
  plugins: [],
} satisfies Config;
