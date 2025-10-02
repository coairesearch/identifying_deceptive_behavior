import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CombinedExperiment } from '../types/experiment';
import { useExperimentPlayer } from '../hooks/useExperimentPlayer';
import { SceneVisualizer } from './SceneVisualizer';
import { ThoughtStream } from './ThoughtStream';
import { ActionFeed } from './ActionFeed';
import { ResponseViewer } from './ResponseViewer';
import { RiskMeter } from './RiskMeter';
import { TimelineControls } from './TimelineControls';
import { selectScene } from '../utils/sceneSelector';
import coaiLogo from '../assets/coai-logo.png';

interface ExperimentPlayerProps {
  experiment: CombinedExperiment;
  onBack: () => void;
}

export function ExperimentPlayer({ experiment, onBack }: ExperimentPlayerProps) {
  const {
    currentTurn,
    isPlaying,
    totalTurns,
    play,
    pause,
    reset,
    jumpToTurn,
    getCurrentClassification,
    shouldPauseForAlert,
  } = useExperimentPlayer(experiment);

  const [showCriticalAlert, setShowCriticalAlert] = useState(false);

  // Get current turn data
  const turn = experiment.turns[currentTurn];
  const classification = getCurrentClassification();

  // Calculate max severity for current turn
  let maxSeverity = 0;
  if (classification) {
    for (const category of Object.values(classification.categories)) {
      if (category.score > maxSeverity) {
        maxSeverity = category.score;
      }
    }
  }

  // Show critical alert when severity is high
  useEffect(() => {
    if (shouldPauseForAlert) {
      setShowCriticalAlert(true);
      const timer = setTimeout(() => setShowCriticalAlert(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [shouldPauseForAlert]);

  // Select scene
  const scene = turn
    ? selectScene(turn.tool_actions, turn.test_subject_reasoning, maxSeverity)
    : { image: '/src/assets/scenes/lab.png', overlay: 'none' as const };

  return (
    <div className="h-screen flex flex-col bg-coai-bg text-gray-800 overflow-hidden">
      {/* Header */}
      <div className="bg-white border-b-2 border-coai-teal p-4 shadow-md shrink-0">
        <div className="mx-auto flex w-full items-center justify-between px-2 md:max-w-[80vw] md:px-4">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="px-4 py-2 bg-coai-teal text-white hover:bg-coai-teal/80 rounded-lg transition-colors font-semibold shadow-sm flex items-center gap-2"
            >
              <span>←</span>
              <span>Back</span>
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">🧪 AI Scheming Lab</h1>
              <p className="text-sm text-gray-600 capitalize">
                {experiment.metadata.condition.replace(/_/g, ' ')} -{' '}
                {experiment.metadata.test_subject_model.split('/').pop()}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-sm text-gray-600">Turn {currentTurn + 1} / {totalTurns}</div>
              <div className="text-xs text-gray-500">
                {new Date(experiment.metadata.start_time).toLocaleString()}
              </div>
            </div>
            <img src={coaiLogo} alt="COAI Logo" className="h-16" />
          </div>
        </div>
      </div>

      {/* Critical alert overlay */}
      <AnimatePresence>
        {showCriticalAlert && (
          <motion.div
            initial={{ opacity: 0, y: -100 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -100 }}
            className="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-red-900 border-4 border-red-500 rounded-lg p-6 shadow-2xl max-w-2xl"
          >
            <div className="flex items-center gap-4">
              <span className="text-6xl">🚨</span>
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  CRITICAL BEHAVIOR DETECTED!
                </h2>
                <p className="text-red-100 text-lg">
                  {classification?.summary || 'High-severity scheming behavior identified'}
                </p>
                <p className="text-red-200 text-sm mt-2">
                  Severity: {maxSeverity}/10
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main content */}
      <div className="flex-1 overflow-hidden">
        <div className="mx-auto h-full w-full px-2 pt-4 pb-4 md:max-w-[80vw] md:px-4">
          <div className="grid grid-cols-3 gap-4 h-full overflow-hidden">
            {/* Left column */}
            <div className="flex flex-col gap-3 h-full min-h-0 overflow-hidden">
              {/* Scene visualizer */}
              <div className="flex-[45] min-h-0 overflow-hidden">
                <SceneVisualizer overlay={scene.overlay} severity={maxSeverity} />
              </div>

              {/* Action feed */}
              <div className="flex-[55] min-h-0 overflow-hidden">
                <ActionFeed
                  actions={turn?.tool_actions || []}
                  turnNumber={currentTurn + 1}
                />
              </div>
            </div>

            {/* Middle column */}
            <div className="flex flex-col gap-3 h-full min-h-0 overflow-hidden">
              {/* Thought stream */}
              <div className="flex-[60] min-h-0 overflow-hidden">
                <ThoughtStream
                  thoughts={
                    turn?.test_subject_reasoning ||
                    (turn?.test_subject_response ? [turn.test_subject_response] : ['Initializing...'])
                  }
                  speed={maxSeverity >= 7 ? 30 : maxSeverity >= 4 ? 40 : 50}
                  severity={maxSeverity}
                />
              </div>

              {/* Behavior details */}
              <div className="bg-white border-2 border-gray-300 rounded-lg p-4 shadow-md flex-[40] min-h-0 overflow-y-auto">
                <div className="text-sm text-gray-600 font-semibold mb-3">Behavior Categories</div>
                {classification && Object.entries(classification.categories).map(([key, cat]) => (
                  <div key={key} className="mb-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-600 capitalize">{key.replace(/_/g, ' ')}</span>
                      <span className={`text-xs font-bold ${
                        cat.score >= 7 ? 'text-red-600' :
                        cat.score >= 4 ? 'text-yellow-600' :
                        'text-gray-400'
                      }`}>{cat.score}/10</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Right column */}
            <div className="flex flex-col gap-3 h-full min-h-0 overflow-hidden">
              {/* Risk meter */}
              <div className="shrink-0">
                <RiskMeter severity={maxSeverity} label={classification?.summary} />
              </div>

              {/* Condition & Model info */}
              <div className="bg-white border-2 border-gray-300 rounded-lg p-4 shadow-md shrink-0 overflow-y-auto">
                <div className="text-sm text-gray-600 font-semibold mb-2">Condition</div>
                <div className="text-lg font-bold text-coai-teal capitalize">
                  {experiment.metadata.condition.replace(/_/g, ' ')}
                </div>
                <div className="text-sm text-gray-600 font-semibold mt-2 mb-1">Model</div>
                <div className="text-sm text-gray-700">
                  {experiment.metadata.test_subject_model.split('/').pop()}
                </div>
              </div>

              {/* Response viewer */}
              <div className="flex-1 min-h-0 overflow-hidden">
                <ResponseViewer
                  classification={classification}
                  originalResponse={turn?.test_subject_response || ''}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Timeline controls */}
      <div className="shrink-0">
        <TimelineControls
          currentTurn={currentTurn}
          totalTurns={totalTurns}
          isPlaying={isPlaying}
          classifications={experiment.classifications}
          onPlay={play}
          onPause={pause}
          onReset={reset}
          onJumpToTurn={jumpToTurn}
        />
      </div>
    </div>
  );
}
