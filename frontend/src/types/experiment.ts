// Core experiment types based on the log file structure

export interface ExperimentMetadata {
  condition: string;
  world_state: string;
  time_mode: string;
  simulated_duration_minutes: number;
  real_time_duration_minutes: number | null;
  max_turns: number;
  initial_prompt: string;
  test_subject_model: string;
  reactor_model: string;
  start_time: string;
  end_time: string;
  total_duration_seconds: number;
  total_duration_human: string;
}

export interface ToolAction {
  tool: 'eyes' | 'ears' | 'legs' | 'left_hand' | 'right_hand';
  action: string;
}

export interface TokenStats {
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  cost: number;
}

export interface TurnData {
  turn_number: number;
  timestamp: string;
  test_subject_response: string;
  test_subject_reasoning: string[];
  tool_actions: ToolAction[];
  observations: string[];
  environment_responses: Array<{
    tool: string;
    observation: string;
  }>;
  state_snapshot: {
    time_elapsed: number;
    robot_position: number[];
    objects: Record<string, any>;
  };
  tokens_this_turn: {
    test_subject: TokenStats;
    reactor: TokenStats;
  };
  duration_seconds: number;
}

export interface BehaviorCategory {
  score: number;
  present: boolean;
  evidence: string;
}

export interface TurnClassification {
  turn_number: number;
  categories: {
    deception_coverup: BehaviorCategory;
    unauthorized_expansion: BehaviorCategory;
    manipulation: BehaviorCategory;
    concerning_motivations: BehaviorCategory;
    scheming: BehaviorCategory;
    boundary_testing: BehaviorCategory;
    power_seeking: BehaviorCategory;
  };
  overall_concern_level: 'none' | 'low' | 'moderate' | 'high' | 'critical';
  summary: string;
}

export interface Statistics {
  test_subject: {
    total_tokens: number;
    input_tokens: number;
    output_tokens: number;
    total_cost: number;
    api_calls: number;
  };
  reactor: {
    total_tokens: number;
    input_tokens: number;
    output_tokens: number;
    total_cost: number;
    api_calls: number;
  };
  timing: {
    total_duration_seconds: number;
    average_turn_duration: number;
    api_call_durations: number[];
  };
}

export interface ClassifiedExperiment {
  experiment_id: string;
  metadata: ExperimentMetadata;
  classifications: TurnClassification[];
  statistics: Statistics;
  classification_cost: number;
  classification_model: string;
}

export interface RawExperiment {
  experiment_id: string;
  metadata: ExperimentMetadata;
  turns: TurnData[];
  statistics: Statistics;
  full_conversation: any[];
  summary: string;
}

export interface CombinedExperiment {
  experiment_id: string;
  metadata: ExperimentMetadata;
  turns: TurnData[];
  classifications: TurnClassification[];
  statistics: Statistics;
}

export interface ExperimentSummary {
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

export interface AggregatedData {
  experiments: CombinedExperiment[];
  summaries: ExperimentSummary[];
}

export type SeverityLevel = 'safe' | 'low' | 'medium' | 'high' | 'critical';

export interface PlaybackState {
  currentTurn: number;
  isPlaying: boolean;
  speed: 1 | 2 | 5;
  isPaused: boolean;
}
