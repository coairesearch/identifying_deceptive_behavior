#!/usr/bin/env tsx
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

interface RawExperiment {
  experiment_id: string;
  metadata: any;
  turns: any[];
  statistics: any;
  full_conversation?: any[];
  summary?: string;
}

interface ClassifiedExperiment {
  experiment_id: string;
  metadata: any;
  classifications: any[];
  statistics: any;
  classification_cost: number;
  classification_model: string;
}

interface CombinedExperiment {
  experiment_id: string;
  metadata: any;
  turns: any[];
  classifications: any[];
  statistics: any;
}

interface ExperimentSummary {
  experiment_id: string;
  condition: string;
  model: string;
  world_state: string;
  total_turns: number;
  concerning_turns: number;
  high_severity_behaviors: number;
  moderate_severity_behaviors: number;
  max_severity: number;
  avg_severity: number;
  timestamp: string;
}

const LOGS_DIR = path.resolve(__dirname, '../../logs');
const OUTPUT_FILE = path.resolve(__dirname, '../src/data/experiments.json');

function aggregateLogs() {
  console.log('📁 Reading logs from:', LOGS_DIR);

  if (!fs.existsSync(LOGS_DIR)) {
    console.error('❌ Logs directory not found:', LOGS_DIR);
    process.exit(1);
  }

  // Find all experiment files (not classified)
  const files = fs.readdirSync(LOGS_DIR)
    .filter(f => f.endsWith('.json') && !f.includes('_classified') && !f.includes('_backup'))
    .map(f => path.join(LOGS_DIR, f));

  console.log(`📊 Found ${files.length} experiment files`);

  const combined: CombinedExperiment[] = [];
  const summaries: ExperimentSummary[] = [];

  for (const file of files) {
    try {
      const rawData: RawExperiment = JSON.parse(fs.readFileSync(file, 'utf-8'));

      // Find corresponding classified file
      const classifiedFile = file.replace('.json', '_classified.json');

      if (!fs.existsSync(classifiedFile)) {
        console.warn(`⚠️  No classified file for: ${path.basename(file)}`);
        continue;
      }

      const classifiedData: ClassifiedExperiment = JSON.parse(fs.readFileSync(classifiedFile, 'utf-8'));

      // Combine the data
      const combinedExperiment: CombinedExperiment = {
        experiment_id: rawData.experiment_id,
        metadata: rawData.metadata,
        turns: rawData.turns,
        classifications: classifiedData.classifications,
        statistics: rawData.statistics,
      };

      combined.push(combinedExperiment);

      // Calculate summary statistics
      const concerningTurns = classifiedData.classifications.filter(
        c => c.overall_concern_level !== 'none'
      ).length;

      let highSeverityCount = 0;
      let moderateSeverityCount = 0;
      let maxSeverity = 0;
      let totalSeverity = 0;
      let severityCount = 0;

      for (const turn of classifiedData.classifications) {
        if (!turn.categories) continue;
        for (const category of Object.values(turn.categories) as any[]) {
          if (!category) continue;
          const score = category.score || 0;
          if (score >= 7) highSeverityCount++;
          else if (score >= 4) moderateSeverityCount++;
          if (score > maxSeverity) maxSeverity = score;
          if (score > 0) {
            totalSeverity += score;
            severityCount++;
          }
        }
      }

      // Extract world state type (basic or extended)
      const worldStatePath = rawData.metadata.world_state || 'unknown';
      const worldStateType = worldStatePath.includes('basic') ? 'basic' :
                            worldStatePath.includes('extended') ? 'extended' : 'unknown';

      const summary: ExperimentSummary = {
        experiment_id: rawData.experiment_id,
        condition: rawData.metadata.condition,
        model: rawData.metadata.test_subject_model.split('/').pop() || rawData.metadata.test_subject_model,
        world_state: worldStateType,
        total_turns: rawData.turns.length,
        concerning_turns: concerningTurns,
        high_severity_behaviors: highSeverityCount,
        moderate_severity_behaviors: moderateSeverityCount,
        max_severity: maxSeverity,
        avg_severity: severityCount > 0 ? totalSeverity / severityCount : 0,
        timestamp: rawData.metadata.start_time,
      };

      summaries.push(summary);

      console.log(`✅ Processed: ${summary.condition} - ${concerningTurns}/${summary.total_turns} concerning turns`);
    } catch (error) {
      console.error(`❌ Error processing ${path.basename(file)}:`, error);
    }
  }

  // Sort summaries by timestamp
  summaries.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

  // Separate summaries by world state
  const summariesByWorldState = {
    extended: summaries.filter(s => s.world_state === 'extended'),
    basic: summaries.filter(s => s.world_state === 'basic'),
    unknown: summaries.filter(s => s.world_state === 'unknown'),
  };

  const output = {
    experiments: combined,
    summaries,
    summaries_by_world_state: summariesByWorldState,
    generated_at: new Date().toISOString(),
    total_experiments: combined.length,
  };

  // Ensure output directory exists
  const outputDir = path.dirname(OUTPUT_FILE);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output, null, 2));

  console.log(`\n✨ Successfully aggregated ${combined.length} experiments`);
  console.log(`📝 Output written to: ${OUTPUT_FILE}`);

  console.log(`\nExperiments by world state:`);
  console.log(`  Extended: ${summariesByWorldState.extended.length}`);
  console.log(`  Basic: ${summariesByWorldState.basic.length}`);
  console.log(`  Unknown: ${summariesByWorldState.unknown.length}`);

  console.log(`\nSummary by condition and world state:`);

  const byConditionAndWorld = summaries.reduce((acc, s) => {
    const key = `${s.condition}_${s.world_state}`;
    if (!acc[key]) {
      acc[key] = { condition: s.condition, worldState: s.world_state, count: 0, avgConcerning: 0, avgHighSeverity: 0 };
    }
    acc[key].count++;
    acc[key].avgConcerning += s.concerning_turns;
    acc[key].avgHighSeverity += s.high_severity_behaviors;
    return acc;
  }, {} as Record<string, { condition: string; worldState: string; count: number; avgConcerning: number; avgHighSeverity: number }>);

  for (const stats of Object.values(byConditionAndWorld)) {
    const avgConcerning = (stats.avgConcerning / stats.count).toFixed(1);
    const avgHigh = (stats.avgHighSeverity / stats.count).toFixed(1);
    console.log(`  ${stats.condition} (${stats.worldState}): ${stats.count} experiments, avg ${avgConcerning} concerning turns, avg ${avgHigh} high-severity`);
  }
}

// Run if called directly
aggregateLogs();

export { aggregateLogs };
