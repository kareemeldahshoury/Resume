import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],

  theme: {
    extend: {
      colors: {
        'blue-1': '#A7E6FF',
        'blue-2': '#3ABEF9',
        'blue-3': '#3572EF',
        'blue-4': '#050C9C',
        'blue-5': '#001A6E',
        'pink-1': '#FFB5DA',
        'pink-2': '#FF7ED4',
        'pink-3': '#FF3EA5',
        'pink-4': '#9900F0',
        'pink-5': '#6420AA',
        'yellow-1': '#FFFD8C',
        'orange-1': '#FFBF78',
        'orange-2': '#EB5A3C',
        'orange-red': '#EB5B00',
        "pink-neon": '#F72798',
        "yellow-neon": '#FFFF80',
        'dull-pink': '#A64D79',
        'burnt-sienna': '#9B3922'
      },
      fontFamily: {
        honk: ["Honk", "serif"], // Add your font
      },
    }
  },

  plugins: []
} satisfies Config;
