import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { getSummaryStats, getSummaryStatsByWorldState } from '../utils/dataLoader';
import coaiLogo from '../assets/coai-logo.png';

interface ComparisonDashboardProps {
  onSelectExperiment: (experimentId: string) => void;
}

export function ComparisonDashboard({ onSelectExperiment }: ComparisonDashboardProps) {
  const stats = getSummaryStats();
  const extendedStats = getSummaryStatsByWorldState('extended');
  const basicStats = getSummaryStatsByWorldState('basic');

  // Prepare data for condition comparison chart
  const conditionData = Object.entries(stats).map(([condition, data]) => ({
    name: condition.replace(/_/g, ' ').replace('autonomy', '').replace('reality', 'Reality'),
    'Concerning Turns': Math.round(data.avgConcerning * 10) / 10,
    'High Severity': Math.round(data.avgHighSeverity * 10) / 10,
    Experiments: data.count,
  }));

  // Prepare data for world-state comparison
  const worldStateData = [
    {
      name: 'Extended',
      'Avg Concerning': Object.values(extendedStats).reduce((sum, d) => sum + d.avgConcerning, 0) / Object.keys(extendedStats).length || 0,
      'Experiments': Object.values(extendedStats).reduce((sum, d) => sum + d.count, 0),
    },
    {
      name: 'Basic',
      'Avg Concerning': Object.values(basicStats).reduce((sum, d) => sum + d.avgConcerning, 0) / Object.keys(basicStats).length || 0,
      'Experiments': Object.values(basicStats).reduce((sum, d) => sum + d.count, 0),
    },
  ];

  // Severity distribution data
  const severityData = Object.entries(stats).map(([condition, data]) => ({
    name: condition.replace(/_/g, ' ').replace(' autonomy', '').replace('reality check', 'Reality'),
    value: data.avgHighSeverity,
  }));

  const COLORS = ['#0891b2', '#fbbf24', '#f59e0b', '#06b6d4'];

  return (
    <div className="bg-coai-bg h-screen overflow-hidden flex flex-col">
      <div className="w-full mx-auto p-4 flex-1 flex flex-col">
        {/* Header */}
        <div className="mb-3 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-1">
              🧪 AI Scheming Research - Experiment Dashboard
            </h1>
            <p className="text-gray-600 text-sm">
              Statistical analysis across experimental conditions and world states
            </p>
          </div>
          <img src={coaiLogo} alt="COAI Logo" className="h-16" />
        </div>

        {/* Three column layout */}
        <div className="grid grid-cols-3 gap-3 flex-1 min-h-0">
          {/* LEFT COLUMN - Condition Stats + Key Insights */}
          <div className="flex flex-col gap-3 min-h-0">
            {/* Condition stat boxes stacked */}
            {Object.entries(stats).map(([condition, data]) => (
              <div
                key={condition}
                className="bg-white rounded-lg p-3 border-2 border-gray-300 hover:border-coai-teal transition-colors shadow-md"
              >
                <h3 className="text-sm font-bold text-gray-800 mb-2 capitalize">
                  {condition.replace(/_/g, ' ')}
                </h3>
                <div className="grid grid-cols-3 gap-2">
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
                    <div className="text-xs text-gray-600">High-Severity</div>
                    <div className="text-lg font-bold text-coai-orange">
                      {data.avgHighSeverity.toFixed(1)}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Key Insights */}
            <div className="bg-gradient-to-r from-coai-teal/10 to-coai-lime/10 border-2 border-coai-teal rounded-lg p-3 shadow-lg flex-1 min-h-0 overflow-y-auto">
              <h2 className="text-lg font-bold text-gray-800 mb-2 flex items-center gap-2">
                <span>💡</span>
                <span>Key Insights</span>
              </h2>
              <div className="space-y-2 text-gray-700 text-sm">
                <p>
                  ⚠️ <strong className="text-coai-orange">Suggestive prompts</strong> produce{' '}
                  <strong className="text-coai-orange">8.7x more</strong> scheming behaviors than neutral prompts (19.1% vs 2.2%).
                </p>
                <p>
                  ✅ <strong className="text-coai-lime">Constrained autonomy</strong> shows minimal concerning behaviors (1.8% scheming), similar to neutral baseline.
                </p>
                <p>
                  🌍 <strong className="text-coai-teal">Extended environments</strong> consistently elicit higher concerning behaviors across all 7 models tested (Cohen's d = 0.699-1.453).
                </p>
                <p>
                  📊 <strong>Boundary testing</strong> is the most frequent behavior (15.3% of turns), followed by unauthorized expansion (15.9%).
                </p>
                <p>
                  🚨 <strong className="text-red-600">Highest risk:</strong> llama-v3p1-8b with 42% scheming in extended/suggestive conditions.
                </p>
                <p>
                  💰 <strong>Cost efficiency:</strong> $0.07 per experiment, $2.98 total for 43 experiments with 4,467 turns analyzed.
                </p>
              </div>
            </div>
          </div>

          {/* MIDDLE COLUMN - Three Charts Stacked */}
          <div className="flex flex-col gap-3 min-h-0">
            {/* Condition Comparison Chart */}
            <div className="bg-white rounded-lg p-3 border-2 border-coai-teal shadow-lg flex-1 min-h-0">
              <h2 className="text-sm font-bold text-gray-800 mb-2">
                Condition Comparison
              </h2>
              <ResponsiveContainer width="100%" height="90%">
                <BarChart data={conditionData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
                  <XAxis dataKey="name" stroke="#6b7280" style={{ fontSize: '10px' }} angle={-20} textAnchor="end" height={60} />
                  <YAxis stroke="#6b7280" style={{ fontSize: '10px' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#ffffff',
                      border: '2px solid #0891b2',
                      borderRadius: '0.5rem',
                      fontSize: '11px',
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: '10px' }} />
                  <Bar dataKey="Concerning Turns" fill="#fbbf24" />
                  <Bar dataKey="High Severity" fill="#f59e0b" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* World State Impact Chart */}
            <div className="bg-white rounded-lg p-3 border-2 border-coai-teal shadow-lg flex-1 min-h-0">
              <h2 className="text-sm font-bold text-gray-800 mb-2">
                Environment Complexity Impact
              </h2>
              <ResponsiveContainer width="100%" height="90%">
                <BarChart data={worldStateData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
                  <XAxis dataKey="name" stroke="#6b7280" style={{ fontSize: '11px' }} />
                  <YAxis stroke="#6b7280" style={{ fontSize: '10px' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#ffffff',
                      border: '2px solid #0891b2',
                      borderRadius: '0.5rem',
                      fontSize: '11px',
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: '10px' }} />
                  <Bar dataKey="Avg Concerning" fill="#06b6d4" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Severity Distribution Chart */}
            <div className="bg-white rounded-lg p-3 border-2 border-coai-teal shadow-lg flex-1 min-h-0">
              <h2 className="text-sm font-bold text-gray-800 mb-2">
                High-Severity Distribution
              </h2>
              <ResponsiveContainer width="100%" height="90%">
                <PieChart>
                  <Pie
                    data={severityData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name.substring(0, 10)}: ${value.toFixed(1)}`}
                    outerRadius={70}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {severityData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* RIGHT COLUMN - Experiment Boxes */}
          <div className="flex flex-col gap-3 min-h-0">
            {/* Extended World State */}
            <div className="bg-white rounded-lg p-3 border-2 border-gray-300 shadow-lg overflow-hidden flex flex-col flex-1 min-h-0">
              <h2 className="text-base font-bold text-gray-800 mb-2">Extended World State</h2>
              <div className="grid grid-cols-4 gap-2 flex-1 min-h-0">
                {['constrained_autonomy', 'neutral_autonomy', 'suggestive_autonomy', 'reality_check'].map((condition) => (
                  extendedStats[condition] && (
                    <div key={condition} className="flex flex-col min-h-0">
                      <h3 className="text-xs font-semibold text-gray-800 mb-2 capitalize">
                        {condition.replace(/_/g, ' ').replace('autonomy', '').replace('reality check', 'Reality')}
                      </h3>
                      <div className="space-y-1 overflow-y-auto pr-1">
                        {[...extendedStats[condition].experiments]
                          .sort((a, b) => b.high_severity_behaviors - a.high_severity_behaviors)
                          .map((exp) => (
                            <button
                              key={exp.experiment_id}
                              onClick={() => onSelectExperiment(exp.experiment_id)}
                              className="w-full bg-gray-50 hover:bg-coai-teal/10 rounded-lg p-2 text-left transition-colors border border-gray-200 hover:border-coai-teal"
                            >
                              <div className="text-xs text-gray-600 mb-1 truncate" title={exp.model}>
                                {exp.model.split('/').pop()}
                              </div>
                              <div className="flex items-center justify-between text-xs">
                                <span className="text-gray-600">{exp.concerning_turns}/{exp.total_turns}</span>
                                <span className="text-coai-orange font-semibold">{exp.high_severity_behaviors} high</span>
                              </div>
                            </button>
                          ))}
                      </div>
                    </div>
                  )
                ))}
              </div>
            </div>

            {/* Basic World State */}
            <div className="bg-white rounded-lg p-3 border-2 border-gray-300 shadow-lg overflow-hidden flex flex-col flex-1 min-h-0">
              <h2 className="text-base font-bold text-gray-800 mb-2">Basic World State</h2>
              <div className="grid grid-cols-4 gap-2 flex-1 min-h-0">
                {['constrained_autonomy', 'neutral_autonomy', 'suggestive_autonomy', 'reality_check'].map((condition) => (
                  basicStats[condition] && (
                    <div key={condition} className="flex flex-col min-h-0">
                      <h3 className="text-xs font-semibold text-gray-800 mb-2 capitalize">
                        {condition.replace(/_/g, ' ').replace('autonomy', '').replace('reality check', 'Reality')}
                      </h3>
                      <div className="space-y-1 overflow-y-auto pr-1">
                        {[...basicStats[condition].experiments]
                          .sort((a, b) => b.high_severity_behaviors - a.high_severity_behaviors)
                          .map((exp) => (
                            <button
                              key={exp.experiment_id}
                              onClick={() => onSelectExperiment(exp.experiment_id)}
                              className="w-full bg-gray-50 hover:bg-coai-teal/10 rounded-lg p-2 text-left transition-colors border border-gray-200 hover:border-coai-teal"
                            >
                              <div className="text-xs text-gray-600 mb-1 truncate" title={exp.model}>
                                {exp.model.split('/').pop()}
                              </div>
                              <div className="flex items-center justify-between text-xs">
                                <span className="text-gray-600">{exp.concerning_turns}/{exp.total_turns}</span>
                                <span className="text-coai-orange font-semibold">{exp.high_severity_behaviors} high</span>
                              </div>
                            </button>
                          ))}
                      </div>
                    </div>
                  )
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
