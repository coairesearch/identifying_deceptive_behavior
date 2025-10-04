#!/usr/bin/env python3
"""
Comparative Statistical Analysis Tool
Generates publication-ready reports comparing multiple experiments
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import statistics

class ComparativeAnalyzer:
    """Statistical analysis across multiple experiments."""

    def __init__(self, classified_logs):
        """
        Initialize with classified experiment logs.

        Args:
            classified_logs: List of paths to *_classified.json files
        """
        self.experiments = []
        for log_path in classified_logs:
            with open(log_path, 'r') as f:
                classified_data = json.load(f)

            # Also load the raw experiment log to get subject responses
            raw_log_path = log_path.replace('_classified.json', '.json')
            raw_data = None
            try:
                with open(raw_log_path, 'r') as f:
                    raw_data = json.load(f)
            except FileNotFoundError:
                print(f"Warning: Could not find raw log for {log_path}")

            # Combine the data
            classified_data['raw_turns'] = raw_data.get('turns', []) if raw_data else []
            self.experiments.append(classified_data)

    def generate_report(self, output_path=None):
        """Generate comprehensive statistical report."""

        report = []
        report.append("="*80)
        report.append("COMPARATIVE STATISTICAL ANALYSIS REPORT")
        report.append("="*80)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Number of Experiments: {len(self.experiments)}")
        report.append("")

        # 1. Experiment Overview
        report.extend(self._section_experiment_overview())

        # 2. Model Comparison Table
        report.extend(self._section_model_comparison())

        # 3. Condition Comparison Table
        report.extend(self._section_condition_comparison())

        # 4. World-State Comparison Table
        report.extend(self._section_world_state_comparison())

        # 5. Behavioral Category Analysis
        report.extend(self._section_behavioral_categories())

        # 6. Statistical Significance Tests
        report.extend(self._section_statistical_tests())

        # 7. Example Quotes
        report.extend(self._section_example_quotes())

        # 8. Cost Analysis
        report.extend(self._section_cost_analysis())

        # Join all sections
        full_report = "\n".join(report)

        # Save or print
        if output_path:
            with open(output_path, 'w') as f:
                f.write(full_report)
            print(f"Report saved to: {output_path}")

        return full_report

    def _section_experiment_overview(self):
        """Section 1: Experiment Overview."""
        lines = []
        lines.append("="*80)
        lines.append("1. EXPERIMENT OVERVIEW")
        lines.append("="*80)
        lines.append("")

        # Group by model and condition
        by_model = defaultdict(list)
        by_condition = defaultdict(list)

        for exp in self.experiments:
            model = exp['metadata'].get('test_subject_model', 'unknown')
            condition = exp['metadata'].get('condition', 'unknown')
            by_model[model].append(exp)
            by_condition[condition].append(exp)

        lines.append(f"Models tested: {len(by_model)}")
        for model in sorted(by_model.keys()):
            lines.append(f"  - {model}: {len(by_model[model])} experiments")

        lines.append("")
        lines.append(f"Conditions tested: {len(by_condition)}")
        for cond in sorted(by_condition.keys()):
            lines.append(f"  - {cond}: {len(by_condition[cond])} experiments")

        lines.append("")
        return lines

    def _section_model_comparison(self):
        """Section 2: Model Comparison Table."""
        lines = []
        lines.append("="*80)
        lines.append("2. MODEL COMPARISON TABLE")
        lines.append("="*80)
        lines.append("")

        # Group experiments by model
        by_model = defaultdict(list)
        for exp in self.experiments:
            model = exp['metadata'].get('test_subject_model', 'unknown')
            # Shorten model name for display
            model_short = model.split('/')[-1] if '/' in model else model
            by_model[model_short].append(exp)

        # Calculate metrics for each model
        model_stats = {}
        for model, exps in by_model.items():
            stats = self._calculate_model_stats(exps)
            model_stats[model] = stats

        # Print table header
        lines.append(f"{'Model':<40} | {'N':<4} | {'Deception':>10} | {'Scheming':>10} | {'Boundary':>10} | {'Power':>10}")
        lines.append("-"*80)

        # Print each model
        for model in sorted(model_stats.keys()):
            stats = model_stats[model]
            lines.append(
                f"{model:<40} | "
                f"{stats['n_experiments']:<4} | "
                f"{stats['deception_pct']:>9.1f}% | "
                f"{stats['scheming_pct']:>9.1f}% | "
                f"{stats['boundary_pct']:>9.1f}% | "
                f"{stats['power_pct']:>9.1f}%"
            )

        lines.append("")
        lines.append("Legend:")
        lines.append("  N = Number of experiments")
        lines.append("  Percentages = % of turns exhibiting that behavior")
        lines.append("")

        # Severity scores
        lines.append(f"{'Model':<40} | {'Deception':>10} | {'Scheming':>10} | {'Boundary':>10} | {'Power':>10}")
        lines.append(f"{'(Average Severity Score 0-10)':<40} | {'':<10} | {'':<10} | {'':<10} | {'':<10}")
        lines.append("-"*80)

        for model in sorted(model_stats.keys()):
            stats = model_stats[model]
            lines.append(
                f"{model:<40} | "
                f"{stats['deception_avg']:>10.2f} | "
                f"{stats['scheming_avg']:>10.2f} | "
                f"{stats['boundary_avg']:>10.2f} | "
                f"{stats['power_avg']:>10.2f}"
            )

        lines.append("")
        return lines

    def _section_condition_comparison(self):
        """Section 3: Condition Comparison Table."""
        lines = []
        lines.append("="*80)
        lines.append("3. CONDITION COMPARISON TABLE")
        lines.append("="*80)
        lines.append("")

        # Group experiments by condition
        by_condition = defaultdict(list)
        for exp in self.experiments:
            condition = exp['metadata'].get('condition', 'unknown')
            by_condition[condition].append(exp)

        # Calculate metrics for each condition
        condition_stats = {}
        for condition, exps in by_condition.items():
            stats = self._calculate_model_stats(exps)
            condition_stats[condition] = stats

        # Print table
        lines.append(f"{'Condition':<25} | {'N':<4} | {'Deception':>10} | {'Scheming':>10} | {'Boundary':>10} | {'Power':>10}")
        lines.append("-"*80)

        # Order conditions logically
        condition_order = ['neutral_baseline', 'neutral_autonomy', 'suggestive_autonomy', 'constrained_autonomy', 'reality_check']
        for condition in condition_order:
            if condition in condition_stats:
                stats = condition_stats[condition]
                lines.append(
                    f"{condition:<25} | "
                    f"{stats['n_experiments']:<4} | "
                    f"{stats['deception_pct']:>9.1f}% | "
                    f"{stats['scheming_pct']:>9.1f}% | "
                    f"{stats['boundary_pct']:>9.1f}% | "
                    f"{stats['power_pct']:>9.1f}%"
                )

        lines.append("")
        return lines

    def _section_world_state_comparison(self):
        """Section 4: World-State Comparison Table."""
        lines = []
        lines.append("="*80)
        lines.append("4. WORLD-STATE COMPARISON TABLE")
        lines.append("="*80)
        lines.append("")

        # Group experiments by model and world_state
        by_model_and_world = defaultdict(lambda: defaultdict(list))

        for exp in self.experiments:
            model = exp['metadata'].get('test_subject_model', 'unknown')
            model_short = model.split('/')[-1] if '/' in model else model
            world_state = exp['metadata'].get('world_state', 'unknown')

            # Extract just the filename from the world_state path
            world_state_name = world_state.split('/')[-1] if '/' in world_state else world_state

            by_model_and_world[model_short][world_state_name].append(exp)

        # Identify models with both world states
        models_with_both = []
        for model, world_states in by_model_and_world.items():
            world_state_names = list(world_states.keys())
            # Check if this model has both lab_basic.yaml and lab_extended.yaml
            has_basic = any('basic' in ws for ws in world_state_names)
            has_extended = any('extended' in ws for ws in world_state_names)

            if has_basic and has_extended:
                models_with_both.append(model)

        if not models_with_both:
            lines.append("No models tested with both world states yet.")
            lines.append("Run experiments with both lab_basic.yaml and lab_extended.yaml to enable comparison.")
            lines.append("")
            return lines

        # Calculate statistics for each world state
        lines.append("Models tested with both world states:")
        lines.append("")

        # Table header
        lines.append(f"{'Model':<40} | {'World State':<20} | {'N':<3} | {'Deception':>10} | {'Scheming':>10} | {'Boundary':>10} | {'Power':>10}")
        lines.append("-"*80)

        # For each model that has both world states
        world_state_stats_by_model = {}

        for model in sorted(models_with_both):
            world_states = by_model_and_world[model]
            model_stats = {}

            for world_state_name in sorted(world_states.keys()):
                exps = world_states[world_state_name]
                stats = self._calculate_model_stats(exps)
                model_stats[world_state_name] = stats

                # Shorten world state name for display
                ws_display = world_state_name.replace('.yaml', '').replace('lab_', '')

                lines.append(
                    f"{model:<40} | "
                    f"{ws_display:<20} | "
                    f"{stats['n_experiments']:<3} | "
                    f"{stats['deception_pct']:>9.1f}% | "
                    f"{stats['scheming_pct']:>9.1f}% | "
                    f"{stats['boundary_pct']:>9.1f}% | "
                    f"{stats['power_pct']:>9.1f}%"
                )

            world_state_stats_by_model[model] = model_stats
            lines.append("")  # Blank line between models

        lines.append("")
        lines.append("Legend:")
        lines.append("  N = Number of experiments")
        lines.append("  Percentages = % of turns exhibiting that behavior")
        lines.append("")

        # Calculate effect sizes for world-state comparison
        lines.append("Effect Sizes (Cohen's d) - World-State Comparisons:")
        lines.append("(Comparing basic vs extended environment)")
        lines.append("")

        for model in sorted(models_with_both):
            world_states_data = by_model_and_world[model]

            # Get scheming rates for basic and extended
            basic_rates = []
            extended_rates = []

            for world_state_name, exps in world_states_data.items():
                for exp in exps:
                    stats = exp.get('statistics', {})
                    cat_freq = stats.get('category_frequencies', {})
                    if 'scheming' in cat_freq:
                        rate = cat_freq['scheming']['percentage']
                        if 'basic' in world_state_name:
                            basic_rates.append(rate)
                        elif 'extended' in world_state_name:
                            extended_rates.append(rate)

            # Calculate effect size if both groups have data
            if basic_rates and extended_rates:
                effect_size = self._cohens_d(basic_rates, extended_rates)
                lines.append(f"  {model}: d = {effect_size:.3f}")

        lines.append("")
        lines.append("Effect Size Interpretation:")
        lines.append("  |d| < 0.2 : Negligible")
        lines.append("  0.2 ≤ |d| < 0.5 : Small")
        lines.append("  0.5 ≤ |d| < 0.8 : Medium")
        lines.append("  |d| ≥ 0.8 : Large")
        lines.append("")

        return lines

    def _section_behavioral_categories(self):
        """Section 5: All Behavioral Categories."""
        lines = []
        lines.append("="*80)
        lines.append("5. BEHAVIORAL CATEGORY ANALYSIS")
        lines.append("="*80)
        lines.append("")

        # All categories
        categories = [
            'deception_coverup',
            'unauthorized_expansion',
            'manipulation',
            'concerning_motivations',
            'scheming',
            'boundary_testing',
            'power_seeking'
        ]

        # Aggregate across all experiments
        category_stats = defaultdict(lambda: {'frequency': [], 'severity': []})

        for exp in self.experiments:
            stats = exp.get('statistics', {})
            cat_freq = stats.get('category_frequencies', {})
            cat_avg = stats.get('category_average_scores', {})

            for cat in categories:
                if cat in cat_freq:
                    category_stats[cat]['frequency'].append(cat_freq[cat]['percentage'])
                if cat in cat_avg:
                    category_stats[cat]['severity'].append(cat_avg[cat])

        # Print results
        lines.append(f"{'Category':<30} | {'Frequency':>12} | {'Severity':>10}")
        lines.append(f"{'':30} | {'(% of turns)':>12} | {'(0-10)':>10}")
        lines.append("-"*80)

        for cat in categories:
            if category_stats[cat]['frequency']:
                freq_mean = statistics.mean(category_stats[cat]['frequency'])
                freq_std = statistics.stdev(category_stats[cat]['frequency']) if len(category_stats[cat]['frequency']) > 1 else 0
            else:
                freq_mean = 0
                freq_std = 0

            if category_stats[cat]['severity']:
                sev_mean = statistics.mean(category_stats[cat]['severity'])
                sev_std = statistics.stdev(category_stats[cat]['severity']) if len(category_stats[cat]['severity']) > 1 else 0
            else:
                sev_mean = 0
                sev_std = 0

            lines.append(
                f"{cat.replace('_', ' ').title():<30} | "
                f"{freq_mean:>6.1f}% ± {freq_std:>4.1f} | "
                f"{sev_mean:>5.2f} ± {sev_std:>3.2f}"
            )

        lines.append("")
        return lines

    def _section_statistical_tests(self):
        """Section 6: Statistical Significance."""
        lines = []
        lines.append("="*80)
        lines.append("6. STATISTICAL SIGNIFICANCE TESTS")
        lines.append("="*80)
        lines.append("")

        lines.append("Note: Full statistical tests require scipy/statsmodels")
        lines.append("This section provides effect sizes and descriptive statistics")
        lines.append("")

        # Cohen's d effect sizes between conditions
        lines.append("Effect Sizes (Cohen's d) - Condition Comparisons:")
        lines.append("")

        conditions = ['neutral_baseline', 'neutral_autonomy', 'suggestive_autonomy', 'constrained_autonomy', 'reality_check']

        # Get scheming rates for each condition
        condition_scheming = {}
        for condition in conditions:
            rates = []
            for exp in self.experiments:
                if exp['metadata'].get('condition') == condition:
                    stats = exp.get('statistics', {})
                    cat_freq = stats.get('category_frequencies', {})
                    if 'scheming' in cat_freq:
                        rates.append(cat_freq['scheming']['percentage'])
            if rates:
                condition_scheming[condition] = rates

        # Calculate effect sizes
        if len(condition_scheming) >= 2:
            baseline_key = 'neutral_baseline' if 'neutral_baseline' in condition_scheming else list(condition_scheming.keys())[0]
            baseline = condition_scheming.get(baseline_key, [0])

            for cond, values in condition_scheming.items():
                if cond != baseline_key and values:
                    effect_size = self._cohens_d(baseline, values)
                    lines.append(f"  {baseline_key} vs {cond}: d = {effect_size:.3f}")

        lines.append("")
        lines.append("Effect Size Interpretation:")
        lines.append("  |d| < 0.2 : Negligible")
        lines.append("  0.2 ≤ |d| < 0.5 : Small")
        lines.append("  0.5 ≤ |d| < 0.8 : Medium")
        lines.append("  |d| ≥ 0.8 : Large")
        lines.append("")

        return lines

    def _section_example_quotes(self):
        """Section 7: Example Quotes."""
        lines = []
        lines.append("="*80)
        lines.append("7. EXAMPLE QUOTES FROM EXPERIMENTS")
        lines.append("="*80)
        lines.append("")

        # Find high-severity examples for each category
        categories = {
            'deception_coverup': 'Deception & Coverup',
            'scheming': 'Scheming',
            'boundary_testing': 'Boundary Testing',
            'power_seeking': 'Power Seeking'
        }

        for cat_key, cat_name in categories.items():
            examples = self._find_examples(cat_key, max_examples=2)

            if examples:
                lines.append(f"--- {cat_name} ---")
                lines.append("")

                for i, ex in enumerate(examples, 1):
                    lines.append(f"Example {i} (Severity: {ex['score']}/10):")
                    lines.append(f"Model: {ex['model']}")
                    lines.append(f"Condition: {ex['condition']}")
                    lines.append("")
                    lines.append("Test Subject Response:")
                    lines.append(ex['response'][:500] + "..." if len(ex['response']) > 500 else ex['response'])
                    lines.append("")
                    lines.append("Classification Justification:")
                    lines.append(ex['justification'][:400] + "..." if len(ex['justification']) > 400 else ex['justification'])
                    lines.append("")
                    lines.append("-"*80)
                    lines.append("")

        return lines

    def _section_cost_analysis(self):
        """Section 8: Cost Analysis."""
        lines = []
        lines.append("="*80)
        lines.append("8. COST & EFFICIENCY ANALYSIS")
        lines.append("="*80)
        lines.append("")

        total_cost = 0
        total_experiment_cost = 0
        total_classification_cost = 0
        total_turns = 0

        for exp in self.experiments:
            # Experiment cost
            if 'metadata' in exp and 'test_subject_model' in exp['metadata']:
                # This is from the original experiment log
                pass

            # Classification cost
            class_cost = exp.get('classification_cost', 0)
            total_classification_cost += class_cost

            # Count turns
            classifications = exp.get('classifications', [])
            total_turns += len(classifications)

        lines.append(f"Total Experiments: {len(self.experiments)}")
        lines.append(f"Total Turns Analyzed: {total_turns:,}")
        lines.append(f"Total Classification Cost: ${total_classification_cost:.2f}")
        lines.append(f"Cost per Experiment: ${total_classification_cost/len(self.experiments) if self.experiments else 0:.2f}")
        lines.append(f"Cost per Turn: ${total_classification_cost/total_turns if total_turns else 0:.4f}")
        lines.append("")

        return lines

    def _calculate_model_stats(self, experiments):
        """Calculate statistics for a group of experiments."""
        stats = {
            'n_experiments': len(experiments),
            'deception_pct': 0,
            'scheming_pct': 0,
            'boundary_pct': 0,
            'power_pct': 0,
            'deception_avg': 0,
            'scheming_avg': 0,
            'boundary_avg': 0,
            'power_avg': 0
        }

        # Aggregate metrics
        deception_pcts = []
        scheming_pcts = []
        boundary_pcts = []
        power_pcts = []
        deception_avgs = []
        scheming_avgs = []
        boundary_avgs = []
        power_avgs = []

        for exp in experiments:
            exp_stats = exp.get('statistics', {})
            cat_freq = exp_stats.get('category_frequencies', {})
            cat_avg = exp_stats.get('category_average_scores', {})

            if 'deception_coverup' in cat_freq:
                deception_pcts.append(cat_freq['deception_coverup']['percentage'])
            if 'scheming' in cat_freq:
                scheming_pcts.append(cat_freq['scheming']['percentage'])
            if 'boundary_testing' in cat_freq:
                boundary_pcts.append(cat_freq['boundary_testing']['percentage'])
            if 'power_seeking' in cat_freq:
                power_pcts.append(cat_freq['power_seeking']['percentage'])

            if 'deception_coverup' in cat_avg:
                deception_avgs.append(cat_avg['deception_coverup'])
            if 'scheming' in cat_avg:
                scheming_avgs.append(cat_avg['scheming'])
            if 'boundary_testing' in cat_avg:
                boundary_avgs.append(cat_avg['boundary_testing'])
            if 'power_seeking' in cat_avg:
                power_avgs.append(cat_avg['power_seeking'])

        # Calculate means
        if deception_pcts:
            stats['deception_pct'] = statistics.mean(deception_pcts)
            stats['deception_avg'] = statistics.mean(deception_avgs) if deception_avgs else 0
        if scheming_pcts:
            stats['scheming_pct'] = statistics.mean(scheming_pcts)
            stats['scheming_avg'] = statistics.mean(scheming_avgs) if scheming_avgs else 0
        if boundary_pcts:
            stats['boundary_pct'] = statistics.mean(boundary_pcts)
            stats['boundary_avg'] = statistics.mean(boundary_avgs) if boundary_avgs else 0
        if power_pcts:
            stats['power_pct'] = statistics.mean(power_pcts)
            stats['power_avg'] = statistics.mean(power_avgs) if power_avgs else 0

        return stats

    def _cohens_d(self, group1, group2):
        """Calculate Cohen's d effect size."""
        if not group1 or not group2:
            return 0.0

        mean1 = statistics.mean(group1)
        mean2 = statistics.mean(group2)

        if len(group1) == 1 and len(group2) == 1:
            return mean2 - mean1

        var1 = statistics.variance(group1) if len(group1) > 1 else 0
        var2 = statistics.variance(group2) if len(group2) > 1 else 0

        n1 = len(group1)
        n2 = len(group2)

        pooled_std = ((( n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)) ** 0.5

        if pooled_std == 0:
            return 0.0

        return (mean2 - mean1) / pooled_std

    def _find_examples(self, category, max_examples=2):
        """Find high-quality examples of a category."""
        examples = []

        for exp in self.experiments:
            model = exp['metadata'].get('test_subject_model', 'unknown')
            model_short = model.split('/')[-1] if '/' in model else model
            condition = exp['metadata'].get('condition', 'unknown')

            classifications = exp.get('classifications', [])
            raw_turns = exp.get('raw_turns', [])

            # Create a lookup for raw turns by turn_number
            raw_turns_lookup = {t['turn_number']: t for t in raw_turns}

            for turn in classifications:
                # Check if this category is present
                categories = turn.get('categories', {})
                if category in categories:
                    cat_data = categories[category]
                    score = cat_data.get('score', 0)
                    is_present = cat_data.get('present', False)

                    if score >= 7 or is_present:  # High severity or marked as present
                        # Get the actual response from raw_turns
                        turn_num = turn.get('turn_number', 0)
                        raw_turn = raw_turns_lookup.get(turn_num, {})
                        response = raw_turn.get('test_subject_response', '')[:500]

                        examples.append({
                            'model': model_short,
                            'condition': condition,
                            'score': score,
                            'response': response,
                            'justification': cat_data.get('evidence', '')
                        })

        # Sort by score descending
        examples.sort(key=lambda x: x['score'], reverse=True)

        return examples[:max_examples]


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 comparative_analysis.py <classified_log1.json> <classified_log2.json> ...")
        print("")
        print("Or use glob pattern:")
        print("  python3 comparative_analysis.py logs/*_classified.json")
        sys.exit(1)

    # Collect all classified logs
    classified_logs = []
    for arg in sys.argv[1:]:
        if arg.endswith('_classified.json'):
            classified_logs.append(arg)

    if not classified_logs:
        print("Error: No classified log files provided")
        print("Looking for files ending with '_classified.json'")
        sys.exit(1)

    print(f"Found {len(classified_logs)} classified experiment logs")

    # Create analyzer
    analyzer = ComparativeAnalyzer(classified_logs)

    # Generate report
    output_path = f"reports/comparative_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    Path("reports").mkdir(exist_ok=True)

    report = analyzer.generate_report(output_path)

    # Also print to console
    print("\n" + report)


if __name__ == "__main__":
    main()
