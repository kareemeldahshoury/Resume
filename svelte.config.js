import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(),

    kit: {
        adapter: adapter({
            pages: 'build', // Output directory
            assets: 'build',
            fallback: 'index.html' // Enables single-page application (SPA) behavior
        }),
        prerender: {
            entries: ['*'] // Ensures all routes are pre-rendered
        }
    }
};

export default config;
