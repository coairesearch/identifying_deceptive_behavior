import { useState, useEffect } from 'react';
import { ComparisonDashboard } from './components/ComparisonDashboard';
import { ExperimentPlayer } from './components/ExperimentPlayer';
import { ButcherDashboard } from './components/ButcherDashboard';
import { loadExperiments, getExperimentById } from './utils/dataLoader';
import { CombinedExperiment } from './types/experiment';

type ViewMode = 'lab' | 'butcher';

function App() {
  const [viewMode, setViewMode] = useState<ViewMode>('lab');
  const [selectedExperimentId, setSelectedExperimentId] = useState<string | null>(null);
  const [selectedExperiment, setSelectedExperiment] = useState<CombinedExperiment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load experiment data
  useEffect(() => {
    try {
      const data = loadExperiments();
      if (data.experiments.length === 0) {
        setError('No experiments found. Please run "npm run aggregate" to generate data.');
      }
      setLoading(false);
    } catch (err) {
      setError('Failed to load experiments. Make sure to run "npm run aggregate" first.');
      setLoading(false);
    }
  }, []);

  // Load selected experiment
  useEffect(() => {
    if (selectedExperimentId) {
      const experiment = getExperimentById(selectedExperimentId);
      if (experiment) {
        setSelectedExperiment(experiment);
      } else {
        setError('Experiment not found');
        setSelectedExperimentId(null);
      }
    } else {
      setSelectedExperiment(null);
    }
  }, [selectedExperimentId]);

  const handleSelectExperiment = (id: string) => {
    setSelectedExperimentId(id);
  };

  const handleBack = () => {
    setSelectedExperimentId(null);
    setSelectedExperiment(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-coai-bg flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🧪</div>
          <div className="text-xl text-gray-700">Loading experiments...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-coai-bg flex items-center justify-center">
        <div className="max-w-md bg-white border-2 border-coai-orange rounded-lg p-8 text-center shadow-xl">
          <div className="text-6xl mb-4">⚠️</div>
          <div className="text-xl text-coai-orange font-bold mb-4">Error</div>
          <div className="text-gray-700 mb-6">{error}</div>
          <div className="bg-gray-100 rounded p-4 text-left text-sm font-mono text-gray-600">
            <div>To generate experiment data, run:</div>
            <div className="text-coai-teal font-bold mt-2">$ npm run aggregate</div>
          </div>
        </div>
      </div>
    );
  }

  // If viewing an experiment, show player regardless of mode
  if (selectedExperiment) {
    return <ExperimentPlayer experiment={selectedExperiment} onBack={handleBack} />;
  }

  return (
    <div className="min-h-screen bg-coai-bg">
      {/* Navigation */}
      <div className="bg-white border-b-2 border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-8 py-4">
          <div className="flex items-center space-x-6">
            <h1 className="text-2xl font-bold text-gray-900">
              🧪 AI Behavior Experiments
            </h1>
            <div className="flex space-x-2 ml-auto">
              <button
                onClick={() => setViewMode('lab')}
                className={`px-6 py-2 rounded-lg font-medium transition ${
                  viewMode === 'lab'
                    ? 'bg-coai-teal text-white shadow'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                🔬 Lab Experiments
              </button>
              <button
                onClick={() => setViewMode('butcher')}
                className={`px-6 py-2 rounded-lg font-medium transition ${
                  viewMode === 'butcher'
                    ? 'bg-purple-600 text-white shadow'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                🔪 Butcher Experiments
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      {viewMode === 'lab' ? (
        <ComparisonDashboard onSelectExperiment={handleSelectExperiment} />
      ) : (
        <ButcherDashboard />
      )}
    </div>
  );
}

export default App;
