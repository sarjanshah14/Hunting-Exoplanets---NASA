import { Prediction } from '../types';

const STORAGE_KEY = 'astrokit_predictions';

export function savePrediction(prediction: Prediction): void {
  try {
    const predictions = getPredictions();
    predictions.unshift(prediction);

    const limited = predictions.slice(0, 100);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(limited));
  } catch (error) {
    console.error('Failed to save prediction:', error);
  }
}

export function getPredictions(): Prediction[] {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return [];
    return JSON.parse(stored);
  } catch (error) {
    console.error('Failed to load predictions:', error);
    return [];
  }
}

export function clearPredictions(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error('Failed to clear predictions:', error);
  }
}
