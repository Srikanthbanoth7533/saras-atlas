import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        command: {
          950: "#070B11",
          900: "#0B0F17",
          850: "#101622",
          800: "#151D2C",
          750: "#1A2538",
          700: "#22314A",
          600: "#2F4263",
          500: "#445E8C",
        },
        accent: {
          cyan: "#06B6D4",
          indigo: "#6366F1",
          emerald: "#10B981",
          amber: "#F59E0B",
          rose: "#EF4444",
          purple: "#A855F7",
        },
      },
      fontFamily: {
        mono: ["var(--font-mono)", "JetBrains Mono", "Menlo", "Courier New", "monospace"],
        sans: ["var(--font-sans)", "Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
