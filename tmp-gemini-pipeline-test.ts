import 'dotenv/config';
import { getAIMealSuggestionsWithPhotos } from './src/geminiApi.ts';

const user = {
  age: 28,
  gender: 'Male' as const,
  height: 175,
  weight: 75,
  targetWeight: 72,
  activityLevel: 'Moderate' as const,
  caloriesTarget: 2200,
  units: 'Metric' as const,
  experienceLevel: 'Intermediate' as const,
  customGoal: 'Weight Loss' as const,
  customWorkoutFocus: 'Strength' as const
};

(async () => {
  try {
    const meals = await getAIMealSuggestionsWithPhotos(user);
    const output = meals.map(m => ({
      recipeName: m.recipeName,
      imageProvider: m.imageProvider,
      imageUrlLength: m.imageUrl?.length,
      imageUrlPreview: (m.imageUrl || '').substring(0, 80)
    }));
    console.log(JSON.stringify(output, null, 2));
    const names = meals.map(m => m.recipeName);
    const uniqueNames = new Set(names);
    const urls = meals.map(m => m.imageUrl);
    const uniqueUrls = new Set(urls);
    console.log('mealCount', meals.length, 'uniqueMeals', uniqueNames.size, 'uniqueUrls', uniqueUrls.size);
  } catch (error) {
    console.error('Pipeline test failed:', error);
    process.exit(1);
  }
})();
