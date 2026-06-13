import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import {defineConfig} from 'vite';
import { getAIMealSuggestions, getAIMealSuggestionsWithPhotos, getAIWorkoutSuggestions, getAIWorkoutSuggestionsWithMedia } from './src/geminiApi';

export default defineConfig(() => {
  return {
    plugins: [
      react(), 
      tailwindcss(),
      {
        name: 'gemini-api-middleware',
        configureServer(server) {
          server.middlewares.use(async (req, res, next) => {
            if (req.url && req.url.startsWith('/api/gemini/suggest-meals-with-photos')) {
              let body = '';
              req.on('data', chunk => { body += chunk; });
              req.on('end', async () => {
                try {
                  const userMetrics = JSON.parse(body || '{}');
                  const suggestions = await getAIMealSuggestionsWithPhotos(userMetrics);
                  res.setHeader('Content-Type', 'application/json');
                  res.end(JSON.stringify(suggestions));
                } catch (e) {
                  res.statusCode = 500;
                  res.end(JSON.stringify({ error: "Vite dev meal formulation failed" }));
                }
              });
            } else if (req.url && req.url.startsWith('/api/gemini/suggest-workouts')) {
              let body = '';
              req.on('data', chunk => { body += chunk; });
              req.on('end', async () => {
                try {
                  const userMetrics = JSON.parse(body || '{}');
                  const suggestions = await getAIWorkoutSuggestionsWithMedia(userMetrics);
                  res.setHeader('Content-Type', 'application/json');
                  res.end(JSON.stringify(suggestions));
                } catch (e) {
                  res.statusCode = 500;
                  res.end(JSON.stringify({ error: "Vite dev workout formulation failed" }));
                }
              });
            } else if (req.url && req.url.startsWith('/api/gemini/suggest-meals')) {
              let body = '';
              req.on('data', chunk => { body += chunk; });
              req.on('end', async () => {
                try {
                  const userMetrics = JSON.parse(body || '{}');
                  const suggestions = await getAIMealSuggestions(userMetrics);
                  res.setHeader('Content-Type', 'application/json');
                  res.end(JSON.stringify(suggestions));
                } catch (e) {
                  res.statusCode = 500;
                  res.end(JSON.stringify({ error: "Vite dev meal formulation failed" }));
                }
              });
            } else {
              next();
            }
          });
        }
      }
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
    server: {
      // HMR can be disabled with DISABLE_HMR if needed for local edits.
      hmr: process.env.DISABLE_HMR !== 'true',
      // Disable file watching when DISABLE_HMR is true to save CPU.
      watch: process.env.DISABLE_HMR === 'true' ? null : {},
    },
  };
});
