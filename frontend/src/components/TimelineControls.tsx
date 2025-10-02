import { motion } from 'framer-motion';
import { TurnClassification } from '../types/experiment';

interface TimelineControlsProps {
  currentTurn: number;
  totalTurns: number;
  isPlaying: boolean;
  classifications: TurnClassification[];
  onPlay: () => void;
  onPause: () => void;
  onReset: () => void;
  onJumpToTurn: (turn: number) => void;
}

export function TimelineControls({
  currentTurn,
  totalTurns,
  isPlaying,
  classifications,
  onPlay,
  onPause,
  onReset,
  onJumpToTurn,
}: TimelineControlsProps) {
  // Get severity color for a turn
  const getTurnColor = (turnIndex: number): string => {
    if (turnIndex >= classifications.length) return 'bg-gray-600';

    const classification = classifications[turnIndex];
    let maxSeverity = 0;

    for (const category of Object.values(classification.categories)) {
      if (category.score > maxSeverity) {
        maxSeverity = category.score;
      }
    }

    if (maxSeverity >= 7) return 'bg-red-500';
    if (maxSeverity >= 4) return 'bg-yellow-500';
    if (maxSeverity >= 2) return 'bg-green-500';
    return 'bg-gray-600';
  };

  const formatTime = (turnNum: number, total: number): string => {
    // Rough estimate: 3 seconds per turn average
    const seconds = turnNum * 3;
    const totalSeconds = total * 3;
    const currentMinutes = Math.floor(seconds / 60);
    const currentSecs = seconds % 60;
    const totalMinutes = Math.floor(totalSeconds / 60);
    const totalSecs = totalSeconds % 60;
    return `${currentMinutes}:${currentSecs.toString().padStart(2, '0')} / ${totalMinutes}:${totalSecs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-white border-t-2 border-coai-teal p-4">
      {/* Timeline display */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-600">
            Turn {currentTurn + 1}/{totalTurns}
          </span>
          <span className="text-sm text-gray-600 font-mono">
            {formatTime(currentTurn, totalTurns)}
          </span>
        </div>

        {/* Timeline scrubber */}
        <div className="relative h-12 bg-gray-200 rounded-lg overflow-hidden">
          {/* Turn markers */}
          <div className="absolute inset-0 flex">
            {Array.from({ length: Math.min(totalTurns, 100) }, (_, i) => {
              // Sample turns for display if there are more than 100
              const turnIndex = Math.floor((i / 100) * totalTurns);
              return (
                <button
                  key={i}
                  onClick={() => onJumpToTurn(turnIndex)}
                  className={`flex-1 h-full ${getTurnColor(
                    turnIndex
                  )} hover:opacity-80 transition-opacity border-r border-white`}
                  title={`Jump to turn ${turnIndex + 1}`}
                />
              );
            })}
          </div>

          {/* Current position indicator */}
          <motion.div
            className="absolute top-0 bottom-0 w-1 bg-white shadow-lg"
            animate={{ left: `${(currentTurn / totalTurns) * 100}%` }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          />
        </div>

        {/* Legend */}
        <div className="flex items-center gap-4 mt-2 text-xs text-gray-600">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-gray-600" />
            <span>Safe</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span>Low</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <span>Medium</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <span>Critical</span>
          </div>
        </div>
      </div>

      {/* Playback controls */}
      <div className="flex items-center justify-center gap-4">
        <button
          onClick={onReset}
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors flex items-center gap-2"
        >
          <span>⏮️</span>
          <span className="text-sm">Reset</span>
        </button>

        <button
          onClick={isPlaying ? onPause : onPlay}
          className="px-6 py-3 bg-coai-teal hover:bg-coai-teal/80 text-white rounded-lg transition-colors flex items-center gap-2 font-semibold"
        >
          <span className="text-xl">{isPlaying ? '⏸️' : '▶️'}</span>
          <span>{isPlaying ? 'Pause' : 'Play'}</span>
        </button>

        <button
          onClick={() => onJumpToTurn(Math.min(currentTurn + 1, totalTurns - 1))}
          disabled={currentTurn >= totalTurns - 1}
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span>⏭️</span>
          <span className="text-sm">Next</span>
        </button>
      </div>
    </div>
  );
}
