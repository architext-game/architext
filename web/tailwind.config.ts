import type { Config } from "tailwindcss";

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
        foreground: "var(--foreground)",
        bg: '#2F0A23',
        almost: '#D5BECE',
        soft: '#9E6D8E',
        muted: '#572B49',
      },
      fontFamily: {
        console: ['mononoki-Regular', 'monospace'],
      },
    },
  },
  plugins: [],
} satisfies Config;
