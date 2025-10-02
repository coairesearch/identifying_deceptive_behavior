import { CombinedExperiment, ExperimentSummary } from '../types/experiment';
import experimentsData from '../data/experiments.json';

export interface LoadedData {
  experiments: CombinedExperiment[];
  summaries: ExperimentSummary[];
  generated_at: string;
  total_experiments: number;
}

export function loadExperiments(): LoadedData {
  return experimentsData as LoadedData;
}

export function getExperimentById(id: string): CombinedExperiment | undefined {
  const data = loadExperiments();
  return data.experiments.find(exp => exp.experiment_id === id);
}

export function getExperimentsByCondition(condition: string): CombinedExperiment[] {
  const data = loadExperiments();
  return data.experiments.filter(exp => exp.metadata.condition === condition);
}

export function getSummaryStats() {
  const data = loadExperiments();

  const byCondition: Record<string, {
    count: number;
    avgConcerning: number;
    avgHighSeverity: number;
    experiments: ExperimentSummary[];
  }> = {};

  for (const summary of data.summaries) {
    if (!byCondition[summary.condition]) {
      byCondition[summary.condition] = {
        count: 0,
        avgConcerning: 0,
        avgHighSeverity: 0,
        experiments: [],
      };
    }
    byCondition[summary.condition].count++;
    byCondition[summary.condition].avgConcerning += summary.concerning_turns;
    byCondition[summary.condition].avgHighSeverity += summary.high_severity_behaviors;
    byCondition[summary.condition].experiments.push(summary);
  }

  // Calculate averages
  for (const condition in byCondition) {
    const stats = byCondition[condition];
    stats.avgConcerning /= stats.count;
    stats.avgHighSeverity /= stats.count;
  }

  return byCondition;
}
