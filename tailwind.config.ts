import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
    },
    typography: () => ({
      nbx: {
        css: [
          {
            ".title1": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 500,
              fontSize: "24px",
              lineHeight: "32px",
            },
            ".title2": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 500,
              fontSize: "20px",
              lineHeight: "normal",
            },
            ".large": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 400,
              fontSize: "18px",
              lineHeight: "24px",
            },
            ".large-pl": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 500,
              fontSize: "18px",
              lineHeight: "24px",
            },
            ".regular": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 400,
              fontSize: "16px",
              lineHeight: "normal",
            },
            ".regular-pl": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 500,
              fontSize: "16px",
              lineHeight: "normal",
            },
            ".medium": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 400,
              fontSize: "14px",
              lineHeight: "normal",
            },
            ".medium-pl": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 500,
              fontSize: "14px",
              lineHeight: "normal",
            },
            ".small": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 400,
              fontSize: "13px",
              lineHeight: "normal",
            },
            ".small-pl": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 500,
              fontSize: "13px",
              lineHeight: "normal",
            },
            ".mini": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 400,
              fontSize: "12px",
              lineHeight: "normal",
            },
            ".mini-pl": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 500,
              fontSize: "12px",
              lineHeight: "normal",
            },
            ".xmini": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 400,
              fontSize: "12px",
              lineHeight: "normal",
            },
            ".xmini-pl": {
              fontFamily: "'Inter', sans-serif",
              fontWeight: 500,
              fontSize: "12px",
              lineHeight: "normal",
            },
          },
        ],
      },
    }),
  },
  plugins: [require("@tailwindcss/typography")],
};
export default config;
