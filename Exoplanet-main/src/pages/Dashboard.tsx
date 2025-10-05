import { useState } from 'react';
import { motion } from 'framer-motion';
import { ModelType, PredictionInput, PredictionResult } from '../types';
import { models } from '../data/models';
import { generatePrediction } from '../utils/prediction';
import { savePrediction } from '../utils/storage';
import { ModelSelection } from '../components/dashboard/ModelSelection';
import { ParameterInput } from '../components/dashboard/ParameterInput';
import { PredictionVisualization } from '../components/dashboard/PredictionVisualization';

export function Dashboard() {
  const [selectedModel, setSelectedModel] = useState<ModelType>('TESS');
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handlePredict = async (input: PredictionInput) => {
    setIsProcessing(true);
    setPrediction(null);

    try {
      const result = await generatePrediction(input, selectedModel);
      setPrediction(result);

      savePrediction({
        id: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
        modelName: selectedModel,
        input,
        result
      });
    } catch (error) {
      console.error('Prediction failed:', error);
      // Handle error - could show a toast notification here
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 bg-clip-text text-transparent mb-4">
            Exoplanet Detection Dashboard
          </h1>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Leverage NASA's machine learning models to analyze planetary candidates and detect exoplanets across the galaxy
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <ModelSelection
              models={models}
              selectedModel={selectedModel}
              onSelectModel={setSelectedModel}
            />
          </div>

          <div className="lg:col-span-2 space-y-8">
            <ParameterInput onPredict={handlePredict} isProcessing={isProcessing} />

            {(prediction || isProcessing) && (
              <PredictionVisualization
                prediction={prediction}
                isProcessing={isProcessing}
                modelName={selectedModel}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
