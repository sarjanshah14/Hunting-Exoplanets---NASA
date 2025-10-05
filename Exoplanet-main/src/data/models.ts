import { ModelInfo, ModelSpecification } from '../types';

export const models: Record<string, ModelInfo> = {
  K2: {
    name: 'K2',
    description: 'Extended Kepler mission observing new fields along the ecliptic plane',
    yearOfOperation: '2014-2018',
    accuracy: 94.2,
    f1Score: 0.91,
    logo: '🛰️'
  },
  TESS: {
    name: 'TESS',
    description: 'Transiting Exoplanet Survey Satellite scanning nearly the entire sky',
    yearOfOperation: '2018-Present',
    accuracy: 96.8,
    f1Score: 0.94,
    logo: '🔭'
  },
  Kepler: {
    name: 'Kepler',
    description: 'Primary mission monitoring 150,000 stars for planetary transits',
    yearOfOperation: '2009-2013',
    accuracy: 93.5,
    f1Score: 0.89,
    logo: '🌟'
  }
};

export const modelSpecifications: Record<string, ModelSpecification> = {
  K2: {
    dataset: {
      size: '37,000 candidates',
      source: 'NASA K2 Mission Archive',
      features: [
        'Light curve characteristics',
        'Transit depth and duration',
        'Signal-to-noise ratio',
        'Stellar parameters',
        'Centroid motion',
        'Secondary eclipse detection'
      ]
    },
    architecture: 'Random Forest Ensemble (500 trees)',
    metrics: {
      accuracy: 94.2,
      precision: 0.92,
      recall: 0.90,
      f1Score: 0.91
    },
    confusionMatrix: [
      [8420, 340],
      [480, 7760]
    ]
  },
  TESS: {
    dataset: {
      size: '52,000 candidates',
      source: 'TESS Mission Data Release',
      features: [
        'Full-frame image photometry',
        'Transit timing variations',
        'Stellar activity indicators',
        'Multi-sector observations',
        'Pixel-level centroid analysis',
        'Background flux measurements'
      ]
    },
    architecture: 'XGBoost Gradient Boosting',
    metrics: {
      accuracy: 96.8,
      precision: 0.95,
      recall: 0.93,
      f1Score: 0.94
    },
    confusionMatrix: [
      [9120, 180],
      [360, 8340]
    ]
  },
  Kepler: {
    dataset: {
      size: '190,000 candidates',
      source: 'Kepler Mission DR25',
      features: [
        'Long-cadence light curves',
        'Data validation metrics',
        'Planet-star radius ratio',
        'Impact parameter',
        'Limb darkening coefficients',
        'Bootstrap false alarm probability'
      ]
    },
    architecture: 'Neural Network (3 hidden layers)',
    metrics: {
      accuracy: 93.5,
      precision: 0.91,
      recall: 0.88,
      f1Score: 0.89
    },
    confusionMatrix: [
      [17200, 800],
      [1300, 15700]
    ]
  }
};
