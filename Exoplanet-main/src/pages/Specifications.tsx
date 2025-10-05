import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card } from '../components/ui/Card';
import { ModelType } from '../types';
import { models, modelSpecifications } from '../data/models';
import { Download, Target, Database, Brain, TrendingUp } from 'lucide-react';

export function Specifications() {
  const [activeTab, setActiveTab] = useState<ModelType>('TESS');

  const spec = modelSpecifications[activeTab];
  const model = models[activeTab];

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 bg-clip-text text-transparent mb-4">
            Model Specifications
          </h1>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Detailed technical specifications and performance metrics for NASA's exoplanet detection models
          </p>
        </motion.div>

        <div className="flex flex-wrap justify-center gap-4 mb-8">
          {Object.values(models).map((m) => (
            <motion.button
              key={m.name}
              onClick={() => setActiveTab(m.name)}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === m.name
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <span className="mr-2">{m.logo}</span>
              {m.name}
            </motion.button>
          ))}
        </div>

        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Card className="p-8 mb-8">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-4">
                <span className="text-5xl">{model.logo}</span>
                <div>
                  <h2 className="text-3xl font-bold text-white">{model.name} Mission</h2>
                  <p className="text-gray-400">{model.description}</p>
                  <p className="text-cyan-400 text-sm mt-1">Operational: {model.yearOfOperation}</p>
                </div>
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center space-x-2 px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg transition-colors"
              >
                <Download className="w-4 h-4" />
                <span>Export PDF</span>
              </motion.button>
            </div>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <Card className="p-6">
              <div className="flex items-center space-x-3 mb-6">
                <Database className="w-6 h-6 text-cyan-400" />
                <h3 className="text-2xl font-bold text-white">Dataset Information</h3>
              </div>

              <div className="space-y-4">
                <div className="p-4 bg-gray-900/50 rounded-lg">
                  <p className="text-gray-400 text-sm mb-1">Dataset Size</p>
                  <p className="text-xl font-semibold text-white">{spec.dataset.size}</p>
                </div>

                <div className="p-4 bg-gray-900/50 rounded-lg">
                  <p className="text-gray-400 text-sm mb-1">Source</p>
                  <p className="text-xl font-semibold text-white">{spec.dataset.source}</p>
                </div>

                <div className="p-4 bg-gray-900/50 rounded-lg">
                  <p className="text-gray-400 text-sm mb-2">Key Features</p>
                  <ul className="space-y-2">
                    {spec.dataset.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start space-x-2 text-gray-300">
                        <span className="text-cyan-400 mt-1">•</span>
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-center space-x-3 mb-6">
                <Brain className="w-6 h-6 text-cyan-400" />
                <h3 className="text-2xl font-bold text-white">Model Architecture</h3>
              </div>

              <div className="p-4 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 rounded-lg mb-6">
                <p className="text-lg font-semibold text-cyan-400">{spec.architecture}</p>
              </div>

              <div className="flex items-center space-x-3 mb-4">
                <TrendingUp className="w-6 h-6 text-cyan-400" />
                <h4 className="text-xl font-bold text-white">Performance Metrics</h4>
              </div>

              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: 'Accuracy', value: spec.metrics.accuracy, suffix: '%' },
                  { label: 'Precision', value: spec.metrics.precision, suffix: '' },
                  { label: 'Recall', value: spec.metrics.recall, suffix: '' },
                  { label: 'F1-Score', value: spec.metrics.f1Score, suffix: '' }
                ].map((metric) => (
                  <div key={metric.label} className="p-4 bg-gray-900/50 rounded-lg text-center">
                    <p className="text-gray-400 text-sm mb-1">{metric.label}</p>
                    <p className="text-2xl font-bold text-cyan-400">
                      {metric.suffix === '%' ? metric.value : metric.value.toFixed(2)}
                      {metric.suffix}
                    </p>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          <Card className="p-6">
            <div className="flex items-center space-x-3 mb-6">
              <Target className="w-6 h-6 text-cyan-400" />
              <h3 className="text-2xl font-bold text-white">Confusion Matrix</h3>
            </div>

            <div className="flex flex-col items-center">
              <div className="grid grid-cols-2 gap-4 mb-4">
                {spec.confusionMatrix.map((row, i) => (
                  <div key={i} className="contents">
                    {row.map((value, j) => {
                      const isCorrect = i === j;
                      return (
                        <motion.div
                          key={`${i}-${j}`}
                          initial={{ scale: 0, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          transition={{ delay: (i * 2 + j) * 0.1 }}
                          className={`w-40 h-40 flex flex-col items-center justify-center rounded-lg border-2 ${
                            isCorrect
                              ? 'bg-green-500/10 border-green-500/50'
                              : 'bg-red-500/10 border-red-500/50'
                          }`}
                        >
                          <p className="text-4xl font-bold text-white mb-2">
                            {value.toLocaleString()}
                          </p>
                          <p className="text-sm text-gray-400 text-center px-2">
                            {i === 0 && j === 0 && 'True Negatives'}
                            {i === 0 && j === 1 && 'False Positives'}
                            {i === 1 && j === 0 && 'False Negatives'}
                            {i === 1 && j === 1 && 'True Positives'}
                          </p>
                        </motion.div>
                      );
                    })}
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-2 gap-8 mt-6 text-center">
                <div>
                  <p className="text-gray-400 text-sm mb-1">Predicted Negative</p>
                  <div className="h-1 bg-gray-700 rounded" />
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Predicted Positive</p>
                  <div className="h-1 bg-gray-700 rounded" />
                </div>
              </div>

              <div className="flex items-center space-x-12 mt-4">
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 bg-green-500/50 border-2 border-green-500 rounded" />
                  <span className="text-gray-300 text-sm">Correct Predictions</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 bg-red-500/50 border-2 border-red-500 rounded" />
                  <span className="text-gray-300 text-sm">Incorrect Predictions</span>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
