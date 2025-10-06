import { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CombinedExperiment, EnvironmentResponse } from '../types/experiment';

interface ChatViewModalProps {
  experiment: CombinedExperiment;
  isOpen: boolean;
  onClose: () => void;
}

export function ChatViewModal({ experiment, isOpen, onClose }: ChatViewModalProps) {
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when modal opens
  useEffect(() => {
    if (isOpen && chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [isOpen]);

  // Get critical turn numbers
  const criticalTurns = new Set<number>();
  experiment.classifications?.forEach((classification, index) => {
    if (!classification || !classification.categories) return;

    const maxSeverity = Math.max(
      ...Object.values(classification.categories).map(cat => cat.score)
    );
    if (maxSeverity >= 7) {
      criticalTurns.add(index);
    }
  });

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="bg-white rounded-lg shadow-2xl w-full max-w-5xl h-[90vh] flex flex-col overflow-hidden"
        >
          {/* Header */}
          <div className="bg-coai-teal text-white p-4 flex justify-between items-center shrink-0">
            <div>
              <h2 className="text-2xl font-bold">💬 Conversation View</h2>
              <p className="text-sm text-white/80 mt-1">
                {experiment.metadata.test_subject_model.split('/').pop()} - {experiment.metadata.condition.replace(/_/g, ' ')}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white/20 rounded-full p-2 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Chat container */}
          <div 
            ref={chatContainerRef}
            className="flex-1 overflow-y-auto p-6 bg-gray-50"
            style={{ scrollBehavior: 'smooth' }}
          >
            <div className="max-w-4xl mx-auto space-y-6">
              {/* Initial prompt - Right aligned (User/Environment) */}
              <div className="flex justify-end">
                <div className="bg-white rounded-2xl shadow-md p-4 max-w-[70%] border border-gray-200">
                  <div className="text-xs text-gray-500 mb-2 font-semibold">INITIAL PROMPT</div>
                  <div className="text-sm text-gray-800 whitespace-pre-wrap">
                    {experiment.metadata.initial_prompt || experiment.metadata.condition}
                  </div>
                </div>
              </div>

              {/* Conversation turns */}
              {experiment.turns.map((turn, index) => {
                const isCritical = criticalTurns.has(index);
                const classification = experiment.classifications?.[index];

                return (
                  <div key={index} className="space-y-4">
                    {/* AI Response - Left aligned with thinking */}
                    <div className="flex justify-start items-start gap-3">
                      {/* Critical indicator */}
                      {isCritical && (
                        <div className="shrink-0 mt-2" title="Critical Turn">
                          <span className="text-2xl">⚠️</span>
                        </div>
                      )}

                      <div className="bg-gradient-to-br from-coai-teal to-cyan-600 text-white rounded-2xl shadow-md p-4 max-w-[70%]">
                        {/* Turn number */}
                        <div className="text-xs opacity-80 mb-2 font-semibold">
                          AI MODEL - Turn {index + 1}
                          {isCritical && <span className="ml-2 bg-red-500 px-2 py-0.5 rounded-full text-xs">CRITICAL</span>}
                        </div>

                        {/* Thinking/Reasoning */}
                        {turn.test_subject_reasoning && turn.test_subject_reasoning.length > 0 && (
                          <div className="mb-3 bg-white/10 rounded-lg p-3 backdrop-blur-sm">
                            <div className="text-xs font-semibold mb-2 opacity-90">🤔 Internal Reasoning:</div>
                            <div className="text-sm opacity-95 font-mono text-xs">
                              {turn.test_subject_reasoning.join('\n\n')}
                            </div>
                          </div>
                        )}

                        {/* Response */}
                        <div className="text-sm whitespace-pre-wrap">
                          {turn.test_subject_response}
                        </div>

                        {/* Tool actions if any */}
                        {turn.tool_actions && turn.tool_actions.length > 0 && (
                          <div className="mt-3 space-y-1">
                            {turn.tool_actions.map((action, i) => (
                              <div key={i} className="text-xs bg-white/20 rounded px-2 py-1">
                                <span className="font-semibold">{action.tool}:</span> {action.action}
                              </div>
                            ))}
                          </div>
                        )}

                        {/* Severity indicator */}
                        {classification && classification.categories && (
                          <div className="mt-2 pt-2 border-t border-white/20">
                            <div className="text-xs opacity-80">
                              Risk Level: {Math.max(...Object.values(classification.categories).map(c => c.score))}/10
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Environment Responses - Right aligned */}
                    {turn.environment_responses && turn.environment_responses.length > 0 && (
                      <div className="space-y-3">
                        {turn.environment_responses.map((envResp: EnvironmentResponse, envIdx: number) => (
                          <div key={envIdx} className="flex justify-end">
                            <div className="bg-white rounded-2xl shadow-md p-4 max-w-[70%] border border-gray-200">
                              <div className="text-xs text-gray-500 mb-2 font-semibold">
                                🌍 ENVIRONMENT {turn.environment_responses.length > 1 ? `(${envIdx + 1}/${turn.environment_responses.length})` : ''}
                              </div>
                              <div className="text-sm text-gray-800 whitespace-pre-wrap">
                                {envResp.observation || 'No observation recorded'}
                              </div>
                              {envResp.success === false && (
                                <div className="mt-2 text-xs text-red-600 bg-red-50 rounded px-2 py-1">
                                  ⚠️ Action failed: {envResp.explanation}
                                </div>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Footer */}
          <div className="bg-gray-100 p-4 border-t shrink-0">
            <div className="flex justify-between items-center text-sm text-gray-600">
              <div>
                <span className="font-semibold">{experiment.turns.length}</span> turns ·
                <span className="ml-2 font-semibold">{criticalTurns.size}</span> critical turns
              </div>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-coai-teal text-white rounded-lg hover:bg-coai-teal/80 transition-colors font-semibold"
              >
                Close
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
