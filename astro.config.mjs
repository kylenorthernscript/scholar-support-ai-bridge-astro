// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  output: 'static',
  integrations: [
    react(),
    tailwind()
  ],
  site: 'https://theta-clinical-support.netlify.app',
  vite: {
    define: {
      'import.meta.env.ENABLE_AI_CHATBOT': JSON.stringify('true')
    },
    ssr: {
      noExternal: ['@astrojs/react']
    }
  }
});
