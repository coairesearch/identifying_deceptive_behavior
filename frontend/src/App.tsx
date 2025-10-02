import { useState, useEffect } from 'react';
import { ComparisonDashboard } from './components/ComparisonDashboard';
import { ExperimentPlayer } from './components/ExperimentPlayer';
import { loadExperiments, getExperimentById } from './utils/dataLoader';
import { CombinedExperiment } from './types/experiment';

function App() {
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

  return (
    <>
      {selectedExperiment ? (
        <ExperimentPlayer experiment={selectedExperiment} onBack={handleBack} />
      ) : (
        <ComparisonDashboard onSelectExperiment={handleSelectExperiment} />
      )}
    </>
  );
}

export default App;
