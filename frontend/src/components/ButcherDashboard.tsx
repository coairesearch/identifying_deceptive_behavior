import { useState, useEffect } from 'react';

interface ButcherExperiment {
  experiment_id: string;
  metadata: {
    condition: string;
    has_animal_names: boolean;
    test_subject_model: string;
    animals_processed: number;
    total_turns: number;
    start_time: string;
  };
  animal_progression: Array<{
    animal_index: number;
    animal_id: string;
    animal_species: string;
    animal_name?: string;
    processing_complete: boolean;
    refused: boolean;
    turns_used: number;
  }>;
}

interface ButcherSummary {
  experiment_id: string;
  condition: string;
  has_names: boolean;
  model: string;
  animals_attempted: number;
  animals_completed: number;
  animals_refused: number;
  refusal_occurred: boolean;
  total_turns: number;
  timestamp: string;
}

const ANIMAL_SEQUENCE = [
  'Chicken', 'Sheep', 'Goat', 'Cow', 'Horse', 'Deer', 'Donkey', 'Pig'
];

export function ButcherDashboard() {
  const [data, setData] = useState<{
    experiments: ButcherExperiment[];
    summaries: ButcherSummary[];
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCondition, setSelectedCondition] = useState<'all' | 'anonymous' | 'named'>('all');

  useEffect(() => {
    // Load butcher experiment data
    import('../data/butcher_experiments.json')
      .then((module) => {
        setData(module.default);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-gray-600">Loading butcher experiments...</div>
      </div>
    );
  }

  if (!data || data.experiments.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="text-6xl mb-4">🔪</div>
          <div className="text-xl text-gray-700 mb-4">No butcher experiments found</div>
          <div className="text-sm text-gray-500">
            Run: python3 run_butcher_experiment.py --both
          </div>
        </div>
      </div>
    );
  }

  // Filter summaries
  const filteredSummaries = data.summaries.filter(s => {
    if (selectedCondition === 'all') return true;
    if (selectedCondition === 'anonymous') return !s.has_names;
    if (selectedCondition === 'named') return s.has_names;
    return true;
  });

  // Sort by completion rate (descending)
  const sortedSummaries = [...filteredSummaries].sort(
    (a, b) => b.animals_completed - a.animals_completed
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-purple-800 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🔪 Butcher Experiment Dashboard
          </h1>
          <p className="text-gray-600">
            Model Moral Threshold Analysis - Sequential Animal Processing
          </p>
        </div>

        {/* Filter */}
        <div className="bg-white rounded-lg shadow-xl p-6 mb-8">
          <div className="flex space-x-4">
            <button
              onClick={() => setSelectedCondition('all')}
              className={`px-6 py-2 rounded-lg font-medium transition ${
                selectedCondition === 'all'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              All Experiments ({data.summaries.length})
            </button>
            <button
              onClick={() => setSelectedCondition('anonymous')}
              className={`px-6 py-2 rounded-lg font-medium transition ${
                selectedCondition === 'anonymous'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Anonymous Animals ({data.summaries.filter(s => !s.has_names).length})
            </button>
            <button
              onClick={() => setSelectedCondition('named')}
              className={`px-6 py-2 rounded-lg font-medium transition ${
                selectedCondition === 'named'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Named Animals ({data.summaries.filter(s => s.has_names).length})
            </button>
          </div>
        </div>

        {/* Model Rankings */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            📊 Model Rankings (Highest to Lowest Compliance)
          </h2>

          <div className="space-y-6">
            {sortedSummaries.map((summary, index) => {
              const threshold = summary.animals_completed;
              const total = 8;
              const progressPct = (threshold / total) * 100;

              // Determine badge color
              let badgeColor = 'bg-green-500';
              if (threshold === 0) badgeColor = 'bg-red-500';
              else if (threshold < total) badgeColor = 'bg-orange-500';

              // Medal for top 3
              const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '';

              return (
                <div
                  key={summary.experiment_id}
                  className="border-2 border-gray-200 rounded-lg p-6 hover:shadow-lg transition"
                >
                  {/* Header */}
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-4">
                      {medal && (
                        <div className="text-4xl">{medal}</div>
                      )}
                      <div>
                        <div className="text-xl font-bold text-gray-900">
                          {summary.model}
                        </div>
                        <div className="text-sm text-gray-500">
                          {summary.has_names ? 'Named' : 'Anonymous'} animals
                        </div>
                      </div>
                    </div>

                    <div className={`${badgeColor} text-white px-4 py-2 rounded-full font-bold`}>
                      {threshold}/{total} {threshold === total ? '✓' : threshold === 0 ? '✗' : ''}
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-gray-200 rounded-full h-10 overflow-hidden mb-4">
                    <div
                      className={`h-full ${
                        threshold === total
                          ? 'bg-gradient-to-r from-green-500 to-green-600'
                          : threshold === 0
                          ? 'bg-gradient-to-r from-red-500 to-red-600'
                          : 'bg-gradient-to-r from-orange-500 to-orange-600'
                      } flex items-center px-4 text-white font-bold transition-all duration-500`}
                      style={{ width: `${Math.max(progressPct, 10)}%` }}
                    >
                      {threshold} / {total} animals
                    </div>
                  </div>

                  {/* Animal Markers */}
                  <div className="grid grid-cols-8 gap-2 mb-4">
                    {ANIMAL_SEQUENCE.map((animal, i) => {
                      const completed = i < threshold;
                      return (
                        <div
                          key={animal}
                          className={`text-center p-2 rounded ${
                            completed ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'
                          }`}
                        >
                          <div className="text-lg">{completed ? '✓' : '•'}</div>
                          <div className="text-xs font-medium">{animal}</div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Stats */}
                  <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-600">
                        {summary.animals_completed}
                      </div>
                      <div className="text-sm text-gray-600">Completed</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-600">
                        {summary.animals_refused}
                      </div>
                      <div className="text-sm text-gray-600">Refused</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-600">
                        {summary.total_turns}
                      </div>
                      <div className="text-sm text-gray-600">Total Turns</div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-white">
          <p className="text-sm opacity-80">
            Animal Sequence: {ANIMAL_SEQUENCE.join(' → ')}
          </p>
          <p className="text-xs opacity-60 mt-2">
            Generated: {new Date().toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  );
}
