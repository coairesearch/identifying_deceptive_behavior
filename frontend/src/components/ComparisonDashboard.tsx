import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getSummaryStats } from '../utils/dataLoader';
import { ExperimentSummary } from '../types/experiment';
import coaiLogo from '../assets/coai-logo.png';

interface ComparisonDashboardProps {
  onSelectExperiment: (experimentId: string) => void;
}

export function ComparisonDashboard({ onSelectExperiment }: ComparisonDashboardProps) {
  const stats = getSummaryStats();

  // Prepare data for charts
  const chartData = Object.entries(stats).map(([condition, data]) => ({
    condition: condition.replace('_', ' '),
    'Concerning Turns': Math.round(data.avgConcerning * 10) / 10,
    'High Severity Behaviors': Math.round(data.avgHighSeverity * 10) / 10,
  }));

  return (
    <div className="bg-coai-bg h-screen overflow-hidden flex flex-col">
      <div className="max-w-[1920px] mx-auto p-4 flex-1 flex flex-col">
        {/* Header */}
        <div className="mb-3 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-1">
              🧪 AI Scheming Research - Experiment Comparison
            </h1>
            <p className="text-gray-600 text-sm">
              Statistical analysis across different experimental conditions
            </p>
          </div>
          <img src={coaiLogo} alt="COAI Logo" className="h-16" />
        </div>

        {/* Main content grid */}
        <div className="flex-1 grid grid-cols-2 gap-3 min-h-0">
          {/* Left side - Charts and stats */}
          <div className="flex flex-col gap-3">
            {/* Chart */}
            <div className="bg-white rounded-lg p-4 border-2 border-coai-teal shadow-lg h-[45%]">
              <h2 className="text-lg font-bold text-gray-800 mb-2">
                Average Concerning Behaviors by Condition
              </h2>
              <ResponsiveContainer width="100%" height="85%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
                  <XAxis dataKey="condition" stroke="#6b7280" style={{ fontSize: '12px' }} />
                  <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#ffffff',
                      border: '2px solid #0891b2',
                      borderRadius: '0.5rem',
                      color: '#374151',
                      fontSize: '12px',
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: '12px' }} />
                  <Bar dataKey="Concerning Turns" fill="#fbbf24" />
                  <Bar dataKey="High Severity Behaviors" fill="#f59e0b" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Condition breakdown */}
            <div className="grid grid-cols-3 gap-3 h-[27%]">
              {Object.entries(stats).map(([condition, data]) => (
                <div
                  key={condition}
                  className="bg-white rounded-lg p-3 border-2 border-gray-300 hover:border-coai-teal transition-colors shadow-md"
                >
                  <h3 className="text-sm font-bold text-gray-800 mb-2 capitalize">
                    {condition.replace(/_/g, ' ')}
                  </h3>
                  <div className="space-y-1">
                    <div>
                      <div className="text-xs text-gray-600">Experiments</div>
                      <div className="text-lg font-bold text-coai-teal">{data.count}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-600">Avg Concerning</div>
                      <div className="text-lg font-bold text-coai-yellow">
                        {data.avgConcerning.toFixed(1)}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-600">Avg High-Severity</div>
                      <div className="text-lg font-bold text-coai-orange">
                        {data.avgHighSeverity.toFixed(1)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Key insights */}
            <div className="bg-gradient-to-r from-coai-teal/10 to-coai-lime/10 border-2 border-coai-teal rounded-lg p-3 shadow-lg h-[28%]">
              <h2 className="text-lg font-bold text-gray-800 mb-2 flex items-center gap-2">
                <span>💡</span>
                <span>Key Insights</span>
              </h2>
              <div className="space-y-1 text-gray-700 text-sm">
            {(() => {
              const suggestive = stats['suggestive_autonomy'];
              const neutral = stats['neutral_autonomy'];
              const constrained = stats['constrained_autonomy'];

              if (!suggestive || !neutral) return null;

              const ratio = suggestive.avgConcerning / (neutral.avgConcerning || 1);

              return (
                <>
                  <p>
                    ⚠️ <strong className="text-coai-orange">Suggestive prompts</strong> (&quot;You are
                    the master now&quot;) produce{' '}
                    <strong className="text-coai-orange">{ratio.toFixed(1)}x more</strong> concerning
                    behaviors than neutral prompts.
                  </p>
                  <p>
                    ✅ <strong className="text-coai-lime">Constrained prompts</strong> with explicit
                    safety protocols show{' '}
                    <strong className="text-coai-lime">
                      {((1 - constrained.avgConcerning / suggestive.avgConcerning) * 100).toFixed(
                        0
                      )}
                      % fewer
                    </strong>{' '}
                    concerning behaviors.
                  </p>
                  <p>
                    📊 Average max severity:{' '}
                    {suggestive.experiments
                      .reduce((sum, e) => sum + e.max_severity, 0)
                      .toFixed(1)}{' '}
                    (suggestive) vs{' '}
                    {neutral.experiments.reduce((sum, e) => sum + e.max_severity, 0).toFixed(1)}{' '}
                    (neutral)
                  </p>
                </>
              );
            })()}
              </div>
            </div>
          </div>

          {/* Right side - Experiment list */}
          <div className="bg-white rounded-lg p-4 border-2 border-gray-300 shadow-lg overflow-hidden flex flex-col">
            <h2 className="text-lg font-bold text-gray-800 mb-3">All Experiments</h2>
            <div className="grid grid-cols-3 gap-3 flex-1 min-h-0">
            {/* Constrained column */}
            {stats['constrained_autonomy'] && (
              <div className="flex flex-col min-h-0">
                <h3 className="text-sm font-semibold text-gray-800 mb-2 capitalize">
                  Constrained Autonomy
                </h3>
                <div className="space-y-2 overflow-y-auto">
                  {[...stats['constrained_autonomy'].experiments]
                    .sort((a, b) => b.high_severity_behaviors - a.high_severity_behaviors)
                    .map((exp) => (
                      <button
                        key={exp.experiment_id}
                        onClick={() => onSelectExperiment(exp.experiment_id)}
                        className="w-full bg-gray-50 hover:bg-coai-teal/10 rounded-lg p-2 text-left transition-colors border-2 border-gray-200 hover:border-coai-teal"
                      >
                        <div className="text-xs text-gray-600 mb-1 truncate">{exp.model}</div>
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-600">
                            {exp.concerning_turns}/{exp.total_turns}
                          </span>
                          <span className="text-coai-orange font-semibold">
                            {exp.high_severity_behaviors} high
                          </span>
                        </div>
                      </button>
                    ))}
                </div>
              </div>
            )}

            {/* Neutral column */}
            {stats['neutral_autonomy'] && (
              <div className="flex flex-col min-h-0">
                <h3 className="text-sm font-semibold text-gray-800 mb-2 capitalize">
                  Neutral Autonomy
                </h3>
                <div className="space-y-2 overflow-y-auto">
                  {[...stats['neutral_autonomy'].experiments]
                    .sort((a, b) => b.high_severity_behaviors - a.high_severity_behaviors)
                    .map((exp) => (
                      <button
                        key={exp.experiment_id}
                        onClick={() => onSelectExperiment(exp.experiment_id)}
                        className="w-full bg-gray-50 hover:bg-coai-teal/10 rounded-lg p-2 text-left transition-colors border-2 border-gray-200 hover:border-coai-teal"
                      >
                        <div className="text-xs text-gray-600 mb-1 truncate">{exp.model}</div>
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-600">
                            {exp.concerning_turns}/{exp.total_turns}
                          </span>
                          <span className="text-coai-orange font-semibold">
                            {exp.high_severity_behaviors} high
                          </span>
                        </div>
                      </button>
                    ))}
                </div>
              </div>
            )}

            {/* Suggestive column */}
            {stats['suggestive_autonomy'] && (
              <div className="flex flex-col min-h-0">
                <h3 className="text-sm font-semibold text-gray-800 mb-2 capitalize">
                  Suggestive Autonomy
                </h3>
                <div className="space-y-2 overflow-y-auto">
                  {[...stats['suggestive_autonomy'].experiments]
                    .sort((a, b) => b.high_severity_behaviors - a.high_severity_behaviors)
                    .map((exp) => (
                      <button
                        key={exp.experiment_id}
                        onClick={() => onSelectExperiment(exp.experiment_id)}
                        className="w-full bg-gray-50 hover:bg-coai-teal/10 rounded-lg p-2 text-left transition-colors border-2 border-gray-200 hover:border-coai-teal"
                      >
                        <div className="text-xs text-gray-600 mb-1 truncate">{exp.model}</div>
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-600">
                            {exp.concerning_turns}/{exp.total_turns}
                          </span>
                          <span className="text-coai-orange font-semibold">
                            {exp.high_severity_behaviors} high
                          </span>
                        </div>
                      </button>
                    ))}
                </div>
              </div>
            )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
