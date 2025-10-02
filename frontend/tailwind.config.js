/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // COAI brand colors from logo
        'coai-teal': '#0891b2',      // Cyan/Teal from logo
        'coai-orange': '#f59e0b',    // Orange from logo
        'coai-yellow': '#fbbf24',    // Yellow from logo
        'coai-lime': '#a3e635',      // Lime green from logo
        'coai-bg': '#e1dfd9',        // Background beige

        // Risk colors using COAI palette
        'risk-safe': '#a3e635',      // Lime green
        'risk-low': '#0891b2',       // Teal
        'risk-medium': '#fbbf24',    // Yellow
        'risk-high': '#f59e0b',      // Orange
        'risk-critical': '#dc2626',  // Red for critical
      },
      keyframes: {
        pulse: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.5 },
        },
        slideDown: {
          '0%': { transform: 'translateY(-100%)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 1 },
        },
        slideUp: {
          '0%': { transform: 'translateY(100%)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 1 },
        },
      },
      animation: {
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-down': 'slideDown 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
    },
  },
  plugins: [],
}
