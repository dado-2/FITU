import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { getAIMealSuggestions, getAIMealSuggestionsWithPhotos, getAIWorkoutSuggestions, getAIWorkoutSuggestionsWithMedia, UserMetricData } from './src/geminiApi';
import dotenv from 'dotenv';

dotenv.config();
console.log(`🔧 Loaded environment variables. GEMINI_API_KEY set: ${!!process.env.GEMINI_API_KEY}`);

const app = express();
app.use(express.json());

const PORT = Number(process.env.PORT || 3000);

// Resolve paths for ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// API Endpoints
app.post('/api/gemini/suggest-meals', async (req, res) => {
  try {
    const userMetrics = req.body as UserMetricData;
    if (!userMetrics) {
      res.status(400).json({ error: "Missing user metric data" });
      return;
    }
    const suggestions = await getAIMealSuggestions(userMetrics);
    res.json(suggestions);
  } catch (error) {
    console.error("Meal proxy handler failed:", error);
    if (error && (error as any).code && (error as any).message) {
      const e = error as any;
      res.status(502).json({ code: e.code, message: e.message, source: e.source || 'gemini', retryable: !!e.retryable });
    } else {
      res.status(500).json({ error: "Internal server error during meal formulation" });
    }
  }
});

app.post('/api/gemini/suggest-meals-with-photos', async (req, res) => {
  try {
    const userMetrics = req.body as UserMetricData;
    if (!userMetrics) {
      res.status(400).json({ error: "Missing user metric data" });
      return;
    }
    console.log('🚀 /api/gemini/suggest-meals-with-photos called.');
    const suggestions = await getAIMealSuggestionsWithPhotos(userMetrics);
    res.json(suggestions);
  } catch (error) {
    console.error("Meal with photos proxy handler failed:", error);
    if (error && (error as any).code && (error as any).message) {
      const e = error as any;
      res.status(502).json({ code: e.code, message: e.message, source: e.source || 'gemini', retryable: !!e.retryable });
    } else {
      res.status(500).json({ error: "Internal server error during meal + image generation" });
    }
  }
});

app.post('/api/gemini/suggest-workouts', async (req, res) => {
  try {
    const userMetrics = req.body as UserMetricData;
    if (!userMetrics) {
      res.status(400).json({ error: "Missing user metric data" });
      return;
    }
    // Attempt to attach short AI-generated demo videos where possible
    const suggestions = await getAIWorkoutSuggestionsWithMedia(userMetrics);
    res.json(suggestions);
  } catch (error) {
    console.error("Workout proxy handler failed:", error);
    if (error && (error as any).code && (error as any).message) {
      const e = error as any;
      res.status(502).json({ code: e.code, message: e.message, source: e.source || 'gemini', retryable: !!e.retryable });
    } else {
      res.status(500).json({ error: "Internal server error during workout formulations" });
    }
  }
});

// Serve static assets in production
const distPath = path.join(__dirname, 'dist');
app.use(express.static(distPath));

// Wildcard fallback for React SPA client-side routing
app.get('*', (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Fitu server running on port ${PORT}`);
});
