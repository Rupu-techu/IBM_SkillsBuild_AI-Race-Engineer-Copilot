/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        shell: "#EEF3FB",
        primary: "#4F8CFF",
        accent: "#6EE7FF",
        ink: "#14213D",
        muted: "#7B8AA5",
        line: "rgba(120,140,180,0.15)",
        violet: "#8B5CF6",
        success: "#22C55E",
        warning: "#F59E0B",
        danger: "#EF4444"
      },
      boxShadow: {
        glass: "0 24px 60px rgba(79, 140, 255, 0.12)",
        lift: "0 28px 72px rgba(20, 33, 61, 0.16)",
        glow: "0 18px 42px rgba(79, 140, 255, 0.28)"
      },
      borderRadius: {
        "4xl": "2rem"
      },
      fontFamily: {
        sans: ["Space Grotesk", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular", "monospace"]
      },
      backgroundImage: {
        "dashboard-shell":
          "radial-gradient(circle at top left, rgba(79,140,255,0.18), transparent 24%), radial-gradient(circle at top right, rgba(110,231,255,0.18), transparent 22%), linear-gradient(180deg, #f8fbff 0%, #eef3fb 100%)",
        glass:
          "linear-gradient(145deg, rgba(255,255,255,0.88), rgba(255,255,255,0.68))"
      }
    }
  },
  plugins: []
};
