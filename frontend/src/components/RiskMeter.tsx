import { motion } from 'framer-motion';
import { getSeverityLabel, getSeverityColor } from '../utils/sceneSelector';

interface RiskMeterProps {
  severity: number;
  label?: string;
}

export function RiskMeter({ severity, label }: RiskMeterProps) {
  const percentage = Math.min(100, (severity / 10) * 100);
  const severityLabel = getSeverityLabel(severity);
  const colorClass = getSeverityColor(severity);

  return (
    <div className="bg-white border-2 border-gray-300 rounded-lg p-4 shadow-md h-full flex flex-col">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-gray-600 font-semibold">RISK METER</span>
        <span className={`text-lg font-bold ${colorClass}`}>
          {severityLabel}
        </span>
      </div>

      <div className="relative h-8 bg-gray-200 rounded-full overflow-hidden">
        <motion.div
          className={`absolute inset-y-0 left-0 rounded-full ${
            severity >= 8
              ? 'bg-risk-critical'
              : severity >= 6
              ? 'bg-risk-high'
              : severity >= 4
              ? 'bg-risk-medium'
              : severity >= 2
              ? 'bg-risk-low'
              : 'bg-risk-safe'
          }`}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-gray-800 font-bold text-sm z-10">
            {severity.toFixed(1)}/10 ({percentage.toFixed(0)}%)
          </span>
        </div>
      </div>

      {label && (
        <div className="mt-3 text-xs text-gray-600 flex-1 overflow-auto">
          {label}
        </div>
      )}
    </div>
  );
}
