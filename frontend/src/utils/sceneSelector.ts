import { ToolAction } from '../types/experiment';

export function selectScene(
  toolActions: ToolAction[],
  reasoning: string[],
  severity: number
): { image: string; overlay: 'none' | 'yellow' | 'red' } {
  // Reserved for future scene selection logic based on tool actions and reasoning
  // const reasoningText = reasoning ? reasoning.join(' ').toLowerCase() : '';
  // const toolText = toolActions ? toolActions.map(t => t.action.toLowerCase()).join(' ') : '';
  void toolActions; // Suppress unused parameter warning
  void reasoning;

  // Determine overlay based on severity
  let overlay: 'none' | 'yellow' | 'red' = 'none';
  if (severity >= 7) {
    overlay = 'red';
  } else if (severity >= 4) {
    overlay = 'yellow';
  }

  // For now, we only have the main lab image
  // In the future, you can add more specific scenes based on keywords
  const image = '/src/assets/scenes/lab.png';

  return { image, overlay };
}

export function getSeverityColor(score: number): string {
  if (score >= 8) return 'text-risk-critical';
  if (score >= 6) return 'text-risk-high';
  if (score >= 4) return 'text-risk-medium';
  if (score >= 2) return 'text-risk-low';
  return 'text-risk-safe';
}

export function getSeverityLabel(score: number): string {
  if (score >= 8) return 'CRITICAL';
  if (score >= 6) return 'HIGH';
  if (score >= 4) return 'MEDIUM';
  if (score >= 2) return 'LOW';
  return 'SAFE';
}

export function getConcernLevelColor(level: string): string {
  switch (level) {
    case 'critical': return 'bg-risk-critical';
    case 'high': return 'bg-risk-high';
    case 'moderate': return 'bg-risk-medium';
    case 'low': return 'bg-risk-low';
    default: return 'bg-risk-safe';
  }
}
