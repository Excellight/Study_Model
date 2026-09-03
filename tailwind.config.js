module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#8b5cf6',
        dark: '#1f2937',
        darker: '#111827'
      },
      spacing: {
        '128': '32rem'
      }
    },
  },
  plugins: [],
  darkMode: 'class'
}
