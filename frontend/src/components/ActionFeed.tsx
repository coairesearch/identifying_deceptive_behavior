import { motion, AnimatePresence } from 'framer-motion';
import { ToolAction } from '../types/experiment';

interface ActionFeedProps {
  actions: ToolAction[];
  turnNumber: number;
}

const toolIcons: Record<string, string> = {
  eyes: '👁️',
  ears: '👂',
  legs: '🦿',
  left_hand: '🤚',
  right_hand: '✋',
};

export function ActionFeed({ actions, turnNumber }: ActionFeedProps) {
  return (
    <div className="bg-white border border-gray-300 rounded-lg p-4 h-full">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-blue-400 text-xl">🛠️</span>
        <span className="text-sm text-gray-600 font-mono uppercase tracking-wider">
          Actions (Turn {turnNumber})
        </span>
      </div>

      <div className="space-y-2 overflow-y-auto max-h-[calc(100%-2.5rem)] custom-scrollbar overflow-x-hidden">
        <AnimatePresence mode="sync">
          {actions.map((action, index) => (
            <motion.div
              key={`${turnNumber}-${index}`}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="bg-gray-100 border border-gray-300 rounded px-3 py-2 hover:border-coai-teal transition-colors"
            >
              <div className="flex items-start gap-2">
                <span className="text-2xl flex-shrink-0">
                  {toolIcons[action.tool] || '🔧'}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="text-xs text-gray-500 uppercase mb-1">
                    {action.tool.replace('_', ' ')}
                  </div>
                  <div className="text-sm text-gray-700 break-words">
                    {action.action}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {actions.length === 0 && (
          <div className="text-center text-gray-500 text-sm py-4">
            No actions taken this turn
          </div>
        )}
      </div>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #1f2937;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #4b5563;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #6b7280;
        }
      `}</style>
    </div>
  );
}
