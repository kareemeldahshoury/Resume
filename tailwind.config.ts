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
        'darkest-purple': '#3D365C', // Yellow-1
        'dark-purple': '#6F70A1', // Orange-1
        'light-purple': '#A2AADB', // Orange-2
        'medium-purple': '#898AC4', // Orange-red
        "lightest-purple": '#C0C9EE', // Pink-Neon
        "yellow-neon": '#FFFF80',
        'dull-pink': '#A64D79',
        'burnt-sienna': '#9B3922'
      },
      fontFamily: {
        honk: ["Honk", "serif"], // Add your font
        'dm-mono': ['DM Mono', 'monospace'],
      },
    }
  },

  plugins: []
} satisfies Config;
