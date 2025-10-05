import { motion, AnimatePresence } from 'framer-motion';
import { Card } from '../ui/Card';
import { PredictionResult } from '../../types';
import { CheckCircle2, XCircle, AlertCircle } from 'lucide-react';

interface PredictionVisualizationProps {
  prediction: PredictionResult | null;
  isProcessing: boolean;
  modelName: string;
}

export function PredictionVisualization({
  prediction,
  isProcessing,
  modelName
}: PredictionVisualizationProps) {
  if (isProcessing) {
    return (
      <Card className="p-8" gradient>
        <div className="flex flex-col items-center justify-center space-y-6">
          <motion.div
            className="relative w-32 h-32"
            animate={{ rotate: 360 }}
            transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
          >
            <div className="absolute inset-0 rounded-full border-4 border-cyan-500/20" />
            <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-cyan-500 border-r-cyan-500" />
            <motion.div
              className="absolute inset-4 rounded-full bg-gradient-to-br from-cyan-500/20 to-blue-500/20"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </motion.div>

          <div className="text-center">
            <h3 className="text-2xl font-bold text-white mb-2">Analyzing Signal</h3>
            <p className="text-gray-400">Processing data with {modelName} model...</p>
          </div>

          <div className="flex space-x-2">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-3 h-3 bg-cyan-500 rounded-full"
                animate={{ y: [0, -10, 0] }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  delay: i * 0.2
                }}
              />
            ))}
          </div>
        </div>
      </Card>
    );
  }

  if (!prediction) return null;

  const statusConfig = {
    candidate: {
      icon: CheckCircle2,
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
      borderColor: 'border-green-500/30',
      label: 'Confirmed Candidate',
      emoji: '🌍'
    },
    false_positive: {
      icon: XCircle,
      color: 'text-red-400',
      bgColor: 'bg-red-500/10',
      borderColor: 'border-red-500/30',
      label: 'False Positive',
      emoji: '❌'
    },
    unknown: {
      icon: AlertCircle,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
      borderColor: 'border-yellow-500/30',
      label: 'Requires Further Analysis',
      emoji: '⚠️'
    }
  };

  const config = statusConfig[prediction.status];
  const Icon = config.icon;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="p-8" gradient>
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 15 }}
              className="inline-block mb-4"
            >
              <div className={`w-32 h-32 rounded-full ${config.bgColor} border-4 ${config.borderColor} flex items-center justify-center text-6xl`}>
                {config.emoji}
              </div>
            </motion.div>

            <motion.h3
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className={`text-3xl font-bold ${config.color} mb-2 flex items-center justify-center space-x-3`}
            >
              <Icon className="w-8 h-8" />
              <span>{config.label}</span>
            </motion.h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="relative"
            >
              <div className="text-center p-6 bg-gray-900/50 rounded-xl border border-gray-700">
                <p className="text-gray-400 text-sm mb-2">Confidence Score</p>
                <div className="relative inline-block">
                  <svg className="w-32 h-32 transform -rotate-90">
                    <circle
                      cx="64"
                      cy="64"
                      r="56"
                      stroke="currentColor"
                      strokeWidth="8"
                      fill="none"
                      className="text-gray-700"
                    />
                    <motion.circle
                      cx="64"
                      cy="64"
                      r="56"
                      stroke="currentColor"
                      strokeWidth="8"
                      fill="none"
                      strokeLinecap="round"
                      className={config.color}
                      initial={{ strokeDasharray: '0 351.858' }}
                      animate={{
                        strokeDasharray: `${prediction.confidence * 351.858} 351.858`
                      }}
                      transition={{ duration: 1, ease: 'easeOut' }}
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <motion.span
                      initial={{ opacity: 0, scale: 0 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.5 }}
                      className={`text-4xl font-bold ${config.color}`}
                    >
                      {Math.round(prediction.confidence * 100)}%
                    </motion.span>
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="flex flex-col justify-center p-6 bg-gray-900/50 rounded-xl border border-gray-700"
            >
              <h4 className="text-lg font-semibold text-white mb-3">Analysis Summary</h4>
              <p className="text-gray-300 leading-relaxed">{prediction.explanation}</p>
            </motion.div>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className={`p-4 ${config.bgColor} border ${config.borderColor} rounded-lg`}
          >
            <p className="text-sm text-gray-300 text-center">
              <span className="font-semibold">Model Used:</span> {modelName} Mission |{' '}
              <span className="font-semibold">Timestamp:</span> {new Date().toLocaleString()}
            </p>
          </motion.div>
        </Card>
      </motion.div>
    </AnimatePresence>
  );
}
