import { useState } from 'react';
import { PredictionInput } from '../../types';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Slider } from '../ui/Slider';
import { Info } from 'lucide-react';

interface ParameterInputProps {
  onPredict: (input: PredictionInput) => void;
  isProcessing: boolean;
}

interface TooltipProps {
  text: string;
}

function Tooltip({ text }: TooltipProps) {
  return (
    <div className="group relative inline-block ml-2">
      <Info className="w-4 h-4 text-gray-500 cursor-help" />
      <div className="invisible group-hover:visible absolute left-6 top-0 w-64 p-2 bg-gray-800 border border-cyan-500/30 rounded-lg text-xs text-gray-300 z-10 shadow-xl">
        {text}
      </div>
    </div>
  );
}

export function ParameterInput({ onPredict, isProcessing }: ParameterInputProps) {
  const [params, setParams] = useState<PredictionInput>({
    nasaConfidence: 0.75,
    signalToNoise: 45,
    transitDepth: 1200,
    orbitalPeriod: 15,
    transitDuration: 3.5,
    planetRadius: 2.5,
    planetTemperature: 850,
    flagNotTransit: false,
    flagStellarEclipse: false,
    flagCentroidOffset: false,
    flagEphemerisMatch: true
  });

  const updateParam = (key: keyof PredictionInput, value: number | boolean) => {
    setParams((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onPredict(params);
  };

  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
        <span className="mr-3">🔬</span>
        Input Parameters
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div className="flex items-center mb-2">
              <label className="text-sm font-medium text-gray-300">NASA Confidence Score</label>
              <Tooltip text="NASA's confidence level in the signal detection (0 = low, 1 = high)" />
            </div>
            <Slider
              min={0}
              max={1}
              step={0.01}
              value={params.nasaConfidence}
              onChange={(e) => updateParam('nasaConfidence', parseFloat(e.target.value))}
            />
            <Input
              type="number"
              min={0}
              max={1}
              step={0.01}
              value={params.nasaConfidence}
              onChange={(e) => updateParam('nasaConfidence', parseFloat(e.target.value))}
              className="mt-2"
            />
          </div>

          <div>
            <div className="flex items-center mb-2">
              <label className="text-sm font-medium text-gray-300">Signal-to-Noise Ratio</label>
              <Tooltip text="Ratio of signal strength to background noise. Higher values indicate clearer signals." />
            </div>
            <Slider
              min={0}
              max={100}
              step={0.1}
              value={params.signalToNoise}
              onChange={(e) => updateParam('signalToNoise', parseFloat(e.target.value))}
            />
            <Input
              type="number"
              min={0}
              max={100}
              step={0.1}
              value={params.signalToNoise}
              onChange={(e) => updateParam('signalToNoise', parseFloat(e.target.value))}
              className="mt-2"
            />
          </div>

          <div>
            <div className="flex items-center mb-2">
              <label className="text-sm font-medium text-gray-300">Transit Depth</label>
              <Tooltip text="Amount of stellar light blocked during transit, measured in parts per million (ppm)" />
            </div>
            <Slider
              min={0}
              max={5000}
              step={10}
              value={params.transitDepth}
              onChange={(e) => updateParam('transitDepth', parseFloat(e.target.value))}
              suffix="ppm"
            />
            <Input
              type="number"
              min={0}
              max={5000}
              step={10}
              value={params.transitDepth}
              onChange={(e) => updateParam('transitDepth', parseFloat(e.target.value))}
              suffix="ppm"
              className="mt-2"
            />
          </div>

          <div>
            <div className="flex items-center mb-2">
              <label className="text-sm font-medium text-gray-300">Orbital Period</label>
              <Tooltip text="Time taken for the planet to complete one orbit around its star" />
            </div>
            <Slider
              min={0.5}
              max={500}
              step={0.5}
              value={params.orbitalPeriod}
              onChange={(e) => updateParam('orbitalPeriod', parseFloat(e.target.value))}
              suffix="days"
            />
            <Input
              type="number"
              min={0.5}
              max={500}
              step={0.5}
              value={params.orbitalPeriod}
              onChange={(e) => updateParam('orbitalPeriod', parseFloat(e.target.value))}
              suffix="days"
              className="mt-2"
            />
          </div>

          <div>
            <div className="flex items-center mb-2">
              <label className="text-sm font-medium text-gray-300">Transit Duration</label>
              <Tooltip text="Length of time the planet blocks the star's light during transit" />
            </div>
            <Slider
              min={0.1}
              max={12}
              step={0.1}
              value={params.transitDuration}
              onChange={(e) => updateParam('transitDuration', parseFloat(e.target.value))}
              suffix="hours"
            />
            <Input
              type="number"
              min={0.1}
              max={12}
              step={0.1}
              value={params.transitDuration}
              onChange={(e) => updateParam('transitDuration', parseFloat(e.target.value))}
              suffix="hours"
              className="mt-2"
            />
          </div>

          <div>
            <div className="flex items-center mb-2">
              <label className="text-sm font-medium text-gray-300">Planet Radius</label>
              <Tooltip text="Estimated size of the planet relative to Earth (1 = Earth-sized)" />
            </div>
            <Slider
              min={0.1}
              max={25}
              step={0.1}
              value={params.planetRadius}
              onChange={(e) => updateParam('planetRadius', parseFloat(e.target.value))}
              suffix="R⊕"
            />
            <Input
              type="number"
              min={0.1}
              max={25}
              step={0.1}
              value={params.planetRadius}
              onChange={(e) => updateParam('planetRadius', parseFloat(e.target.value))}
              suffix="R⊕"
              className="mt-2"
            />
          </div>

          <div>
            <div className="flex items-center mb-2">
              <label className="text-sm font-medium text-gray-300">Planet Temperature</label>
              <Tooltip text="Estimated equilibrium temperature of the planet" />
            </div>
            <Slider
              min={100}
              max={3000}
              step={10}
              value={params.planetTemperature}
              onChange={(e) => updateParam('planetTemperature', parseFloat(e.target.value))}
              suffix="K"
            />
            <Input
              type="number"
              min={100}
              max={3000}
              step={10}
              value={params.planetTemperature}
              onChange={(e) => updateParam('planetTemperature', parseFloat(e.target.value))}
              suffix="K"
              className="mt-2"
            />
          </div>
        </div>

        <div className="border-t border-gray-700 pt-6">
          <h3 className="text-lg font-semibold text-white mb-4">Detection Flags</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { key: 'flagNotTransit', label: 'Not Transit-Like', tooltip: 'Signal does not match expected transit characteristics' },
              { key: 'flagStellarEclipse', label: 'Stellar Eclipse', tooltip: 'Signal may be caused by an eclipsing binary star system' },
              { key: 'flagCentroidOffset', label: 'Centroid Offset', tooltip: 'Light source position shifts during transit (possible background eclipsing binary)' },
              { key: 'flagEphemerisMatch', label: 'Ephemeris Match', tooltip: 'Transit timing matches predicted ephemeris (positive indicator)' }
            ].map(({ key, label, tooltip }) => (
              <label
                key={key}
                className="flex items-center p-3 bg-gray-900/30 rounded-lg cursor-pointer hover:bg-gray-900/50 transition-colors"
              >
                <input
                  type="checkbox"
                  checked={params[key as keyof PredictionInput] as boolean}
                  onChange={(e) => updateParam(key as keyof PredictionInput, e.target.checked)}
                  className="w-5 h-5 rounded border-gray-600 text-cyan-500 focus:ring-cyan-500 focus:ring-offset-gray-900"
                />
                <span className="ml-3 text-gray-300 flex-1">{label}</span>
                <Tooltip text={tooltip} />
              </label>
            ))}
          </div>
        </div>

        <Button type="submit" size="lg" className="w-full" disabled={isProcessing}>
          {isProcessing ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing Signal...
            </span>
          ) : (
            '🚀 Predict Candidate'
          )}
        </Button>
      </form>
    </Card>
  );
}
