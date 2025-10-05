import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';
import { TrendingUp, PieChart as PieChartIcon, BarChart3, Upload } from 'lucide-react';

const scatterData = Array.from({ length: 100 }, () => ({
  radius: Math.random() * 20 + 0.5,
  temperature: Math.random() * 2500 + 200,
  status: Math.random() > 0.3 ? 'candidate' : 'false_positive'
}));

const distributionData = [
  { name: 'Confirmed', value: 68, color: '#22c55e' },
  { name: 'Candidate', value: 145, color: '#06b6d4' },
  { name: 'False Positive', value: 87, color: '#ef4444' }
];

const missionData = [
  { name: 'Kepler', candidates: 2700, confirmed: 2400 },
  { name: 'K2', candidates: 520, confirmed: 380 },
  { name: 'TESS', candidates: 340, confirmed: 180 }
];

const orbitalData = [
  { range: '0-10d', count: 120 },
  { range: '10-50d', count: 85 },
  { range: '50-100d', count: 45 },
  { range: '100-200d', count: 30 },
  { range: '200+d', count: 20 }
];

export function Explorer() {
  const [activeChart, setActiveChart] = useState<'scatter' | 'distribution' | 'missions' | 'orbital'>('scatter');

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 bg-clip-text text-transparent mb-4">
            Data Explorer
          </h1>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Interactive visualizations of exoplanet datasets from Kepler, K2, and TESS missions
          </p>
        </motion.div>

        <div className="flex flex-wrap justify-center gap-4 mb-8">
          {[
            { id: 'scatter', label: 'Radius vs Temperature', icon: TrendingUp },
            { id: 'distribution', label: 'Status Distribution', icon: PieChartIcon },
            { id: 'missions', label: 'Mission Comparison', icon: BarChart3 },
            { id: 'orbital', label: 'Orbital Periods', icon: BarChart3 }
          ].map(({ id, label, icon: Icon }) => (
            <Button
              key={id}
              variant={activeChart === id ? 'primary' : 'outline'}
              onClick={() => setActiveChart(id as typeof activeChart)}
            >
              <Icon className="w-4 h-4 mr-2" />
              {label}
            </Button>
          ))}
        </div>

        <motion.div
          key={activeChart}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Card className="p-8 mb-8">
            <div className="h-96">
              {activeChart === 'scatter' && (
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 20, right: 20, bottom: 60, left: 60 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis
                      type="number"
                      dataKey="temperature"
                      name="Temperature"
                      unit="K"
                      stroke="#9ca3af"
                      label={{ value: 'Planet Temperature (K)', position: 'bottom', offset: 40, fill: '#9ca3af' }}
                    />
                    <YAxis
                      type="number"
                      dataKey="radius"
                      name="Radius"
                      unit="R⊕"
                      stroke="#9ca3af"
                      label={{ value: 'Planet Radius (Earth Radii)', angle: -90, position: 'left', offset: 40, fill: '#9ca3af' }}
                    />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                      labelStyle={{ color: '#fff' }}
                      cursor={{ strokeDasharray: '3 3' }}
                    />
                    <Scatter
                      name="Candidates"
                      data={scatterData.filter((d) => d.status === 'candidate')}
                      fill="#06b6d4"
                      opacity={0.6}
                    />
                    <Scatter
                      name="False Positives"
                      data={scatterData.filter((d) => d.status === 'false_positive')}
                      fill="#ef4444"
                      opacity={0.6}
                    />
                  </ScatterChart>
                </ResponsiveContainer>
              )}

              {activeChart === 'distribution' && (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={distributionData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}`}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {distributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                    />
                    <Legend
                      wrapperStyle={{ paddingTop: '20px' }}
                      iconType="circle"
                    />
                  </PieChart>
                </ResponsiveContainer>
              )}

              {activeChart === 'missions' && (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={missionData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis
                      dataKey="name"
                      stroke="#9ca3af"
                      label={{ value: 'Mission', position: 'bottom', offset: 40, fill: '#9ca3af' }}
                    />
                    <YAxis
                      stroke="#9ca3af"
                      label={{ value: 'Count', angle: -90, position: 'left', offset: 0, fill: '#9ca3af' }}
                    />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                    />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    <Bar dataKey="candidates" fill="#06b6d4" name="Candidates" />
                    <Bar dataKey="confirmed" fill="#22c55e" name="Confirmed" />
                  </BarChart>
                </ResponsiveContainer>
              )}

              {activeChart === 'orbital' && (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={orbitalData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis
                      dataKey="range"
                      stroke="#9ca3af"
                      label={{ value: 'Orbital Period Range', position: 'bottom', offset: 40, fill: '#9ca3af' }}
                    />
                    <YAxis
                      stroke="#9ca3af"
                      label={{ value: 'Number of Planets', angle: -90, position: 'left', offset: 0, fill: '#9ca3af' }}
                    />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                    />
                    <Bar dataKey="count" fill="#8b5cf6" name="Planets" />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </Card>

          <Card className="p-8">
            <div className="flex flex-col md:flex-row items-center justify-between">
              <div className="mb-6 md:mb-0">
                <h3 className="text-2xl font-bold text-white mb-2">Upload Custom Dataset</h3>
                <p className="text-gray-400">
                  Upload your own exoplanet data in CSV format for analysis
                </p>
              </div>

              <div className="flex flex-col items-center p-8 border-2 border-dashed border-gray-700 rounded-lg hover:border-cyan-500 transition-colors cursor-pointer">
                <Upload className="w-12 h-12 text-gray-500 mb-3" />
                <p className="text-gray-400 text-sm">Drop files here or click to browse</p>
                <p className="text-gray-600 text-xs mt-1">CSV format, max 10MB</p>
              </div>
            </div>
          </Card>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <Card className="p-6">
            <div className="text-center">
              <p className="text-gray-400 mb-2">Total Planets Analyzed</p>
              <p className="text-4xl font-bold text-cyan-400">300</p>
            </div>
          </Card>

          <Card className="p-6">
            <div className="text-center">
              <p className="text-gray-400 mb-2">Confirmed Candidates</p>
              <p className="text-4xl font-bold text-green-400">145</p>
            </div>
          </Card>

          <Card className="p-6">
            <div className="text-center">
              <p className="text-gray-400 mb-2">Average Confidence</p>
              <p className="text-4xl font-bold text-blue-400">78%</p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
