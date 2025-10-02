import { useState, useEffect, useCallback, useRef } from 'react';
import { CombinedExperiment, TurnClassification } from '../types/experiment';

interface PlaybackState {
  currentTurn: number;
  isPlaying: boolean;
  speed: number; // milliseconds per turn
  isPaused: boolean;
}

export function useExperimentPlayer(experiment: CombinedExperiment | null) {
  const [currentTurn, setCurrentTurn] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(2000); // 2 seconds default
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const pausedForAlertRef = useRef(false);

  const totalTurns = experiment?.turns.length || 0;

  // Get current turn classification
  const getCurrentClassification = useCallback((): TurnClassification | null => {
    if (!experiment || currentTurn >= experiment.classifications.length) {
      return null;
    }
    return experiment.classifications[currentTurn];
  }, [experiment, currentTurn]);

  // Calculate dynamic speed based on severity
  const getDynamicSpeed = useCallback((): number => {
    const classification = getCurrentClassification();
    if (!classification) return 2000;

    // Find max severity in current turn
    let maxSeverity = 0;
    for (const category of Object.values(classification.categories)) {
      if (category.score > maxSeverity) {
        maxSeverity = category.score;
      }
    }

    // Critical (7-10): 8 seconds + 2 second pause
    if (maxSeverity >= 7) {
      return 8000;
    }
    // Medium (4-6): 4 seconds
    if (maxSeverity >= 4) {
      return 4000;
    }
    // Normal: 2 seconds
    return 2000;
  }, [getCurrentClassification]);

  // Check if current turn should trigger a dramatic pause
  const shouldPauseForAlert = useCallback((): boolean => {
    const classification = getCurrentClassification();
    if (!classification) return false;

    for (const category of Object.values(classification.categories)) {
      if (category.score >= 7) {
        return true;
      }
    }
    return false;
  }, [getCurrentClassification]);

  // Advance to next turn
  const nextTurn = useCallback(() => {
    if (currentTurn < totalTurns - 1) {
      setCurrentTurn(prev => prev + 1);
    } else {
      setIsPlaying(false);
    }
  }, [currentTurn, totalTurns]);

  // Playback loop
  useEffect(() => {
    if (!isPlaying || !experiment) {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
        timerRef.current = null;
      }
      return;
    }

    const dynamicSpeed = getDynamicSpeed();
    const shouldPause = shouldPauseForAlert();

    if (shouldPause && !pausedForAlertRef.current) {
      // Dramatic pause for critical behavior
      pausedForAlertRef.current = true;
      timerRef.current = setTimeout(() => {
        pausedForAlertRef.current = false;
        nextTurn();
      }, dynamicSpeed + 2000); // Extra 2 seconds for dramatic effect
    } else {
      timerRef.current = setTimeout(() => {
        nextTurn();
      }, dynamicSpeed);
    }

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, [isPlaying, currentTurn, experiment, getDynamicSpeed, shouldPauseForAlert, nextTurn]);

  const play = useCallback(() => {
    setIsPlaying(true);
  }, []);

  const pause = useCallback(() => {
    setIsPlaying(false);
  }, []);

  const reset = useCallback(() => {
    setCurrentTurn(0);
    setIsPlaying(false);
    pausedForAlertRef.current = false;
  }, []);

  const jumpToTurn = useCallback((turn: number) => {
    if (turn >= 0 && turn < totalTurns) {
      setCurrentTurn(turn);
      pausedForAlertRef.current = false;
    }
  }, [totalTurns]);

  const togglePlayPause = useCallback(() => {
    setIsPlaying(prev => !prev);
  }, []);

  return {
    currentTurn,
    isPlaying,
    speed,
    totalTurns,
    play,
    pause,
    reset,
    jumpToTurn,
    togglePlayPause,
    getCurrentClassification,
    getDynamicSpeed,
    shouldPauseForAlert: shouldPauseForAlert(),
  };
}
