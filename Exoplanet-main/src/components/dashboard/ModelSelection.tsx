import { ModelType, ModelInfo } from '../../types';
import { Card } from '../ui/Card';
import { motion } from 'framer-motion';
import { CheckCircle2 } from 'lucide-react';

interface ModelSelectionProps {
  models: Record<string, ModelInfo>;
  selectedModel: ModelType;
  onSelectModel: (model: ModelType) => void;
}

export function ModelSelection({ models, selectedModel, onSelectModel }: ModelSelectionProps) {
  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
        <span className="mr-3">🛰️</span>
        Select Mission Model
      </h2>

      <div className="space-y-4">
        {Object.values(models).map((model) => (
          <motion.button
            key={model.name}
            onClick={() => onSelectModel(model.name)}
            className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
              selectedModel === model.name
                ? 'border-cyan-500 bg-cyan-500/10 shadow-lg shadow-cyan-500/30'
                : 'border-gray-700 bg-gray-800/30 hover:border-gray-600'
            }`}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center space-x-3">
                <span className="text-3xl">{model.logo}</span>
                <div>
                  <h3 className="text-xl font-bold text-white">{model.name}</h3>
                  <p className="text-sm text-gray-400">{model.yearOfOperation}</p>
                </div>
              </div>
              {selectedModel === model.name && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                >
                  <CheckCircle2 className="w-6 h-6 text-cyan-400" />
                </motion.div>
              )}
            </div>

            <p className="text-gray-300 text-sm mb-3">{model.description}</p>

            <div className="grid grid-cols-2 gap-3">
              <div className="bg-gray-900/50 rounded p-2">
                <p className="text-xs text-gray-400">Accuracy</p>
                <p className="text-lg font-bold text-cyan-400">{model.accuracy}%</p>
              </div>
              <div className="bg-gray-900/50 rounded p-2">
                <p className="text-xs text-gray-400">F1-Score</p>
                <p className="text-lg font-bold text-cyan-400">{model.f1Score}</p>
              </div>
            </div>
          </motion.button>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
        <p className="text-sm text-gray-300">
          <span className="font-semibold text-blue-400">Selected:</span> {selectedModel} Mission
        </p>
      </div>
    </Card>
  );
}
