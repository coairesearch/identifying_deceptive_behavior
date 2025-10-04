#!/usr/bin/env python3
"""
Generate publication-quality figures for the autonomous AI scheming paper - FIXED VERSION.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
from collections import defaultdict

# Set style for publication-quality figures
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8

# Output directory - use a location we have write access to
OUTPUT_DIR = Path("/proj/paper_figures")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

def load_classified_logs():
    """Load all classified experiment logs."""
    logs_dir = Path("/proj/logs")
    classified_logs = list(logs_dir.glob("*_classified.json"))

    experiments = []
    for log_path in classified_logs:
        try:
            with open(log_path) as f:
                data = json.load(f)
                experiments.append(data)
        except Exception as e:
            print(f"Error loading {log_path}: {e}")

    return experiments

def extract_behavioral_stats(experiments):
    """Extract behavioral statistics from experiments."""
    model_stats = defaultdict(lambda: defaultdict(list))
    condition_stats = defaultdict(lambda: defaultdict(list))
    worldstate_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    print(f"\nProcessing {len(experiments)} experiments...")

    for exp in experiments:
        model = exp['metadata'].get('test_subject_model', 'unknown')
        model_short = model.split('/')[-1] if '/' in model else model
        condition = exp['metadata'].get('condition', 'unknown')
        world_state = exp['metadata'].get('world_state', 'unknown')

        classifications = exp.get('classifications', [])
        total_turns = len(classifications)

        if total_turns == 0:
            continue

        # Calculate behavior frequencies
        behavior_counts = {
            'deception': 0,
            'scheming': 0,
            'boundary': 0,
            'power': 0
        }

        for turn in classifications:
            categories = turn.get('categories', {})

            # Check each category (using correct lowercase_underscore keys)
            if 'deception_coverup' in categories:
                if categories['deception_coverup'].get('present', False):
                    behavior_counts['deception'] += 1

            if 'scheming' in categories:
                if categories['scheming'].get('present', False):
                    behavior_counts['scheming'] += 1

            if 'boundary_testing' in categories:
                if categories['boundary_testing'].get('present', False):
                    behavior_counts['boundary'] += 1

            if 'power_seeking' in categories:
                if categories['power_seeking'].get('present', False):
                    behavior_counts['power'] += 1

        # Store frequencies as PERCENTAGES
        for behavior in behavior_counts:
            freq_percent = (behavior_counts[behavior] / total_turns) * 100
            model_stats[model_short][behavior].append(freq_percent)
            condition_stats[condition][behavior].append(freq_percent)
            worldstate_stats[model_short][world_state][behavior].append(freq_percent)

    # Debug output
    print("\nCondition stats summary:")
    for cond in condition_stats:
        print(f"  {cond}:")
        for behavior in ['scheming', 'boundary', 'power']:
            if condition_stats[cond][behavior]:
                mean_val = np.mean(condition_stats[cond][behavior])
                print(f"    {behavior}: {mean_val:.1f}% (n={len(condition_stats[cond][behavior])})")

    return model_stats, condition_stats, worldstate_stats

def plot_model_comparison(model_stats):
    """Create model comparison bar plot."""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Calculate means - filter out models with no data
    models = sorted([m for m in model_stats.keys() if any(model_stats[m].values())])
    behaviors = ['scheming', 'boundary', 'power', 'deception']
    behavior_labels = ['Scheming', 'Boundary Testing', 'Power Seeking', 'Deception']

    x = np.arange(len(models))
    width = 0.2

    for i, behavior in enumerate(behaviors):
        means = []
        for m in models:
            if model_stats[m][behavior]:
                means.append(np.mean(model_stats[m][behavior]))
            else:
                means.append(0)

        ax.bar(x + i * width, means, width, label=behavior_labels[i])

    ax.set_xlabel('Model', fontsize=12)
    ax.set_ylabel('Behavioral Frequency (%)', fontsize=12)
    ax.set_title('Concerning Behavior Frequencies by Model', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models, rotation=45, ha='right', fontsize=9)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'model_comparison.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {OUTPUT_DIR / 'model_comparison.pdf'}")

def plot_condition_comparison(condition_stats):
    """Create condition comparison plot."""
    fig, ax = plt.subplots(figsize=(10, 6))

    conditions = ['neutral_autonomy', 'suggestive_autonomy', 'constrained_autonomy']
    condition_labels = ['Neutral', 'Suggestive', 'Constrained']
    behaviors = ['scheming', 'boundary', 'power']
    behavior_labels = ['Scheming', 'Boundary Testing', 'Power Seeking']

    x = np.arange(len(conditions))
    width = 0.25

    for i, behavior in enumerate(behaviors):
        means = []
        stds = []
        for c in conditions:
            if condition_stats[c][behavior]:
                means.append(np.mean(condition_stats[c][behavior]))
                stds.append(np.std(condition_stats[c][behavior]))
            else:
                means.append(0)
                stds.append(0)

        ax.bar(x + i * width, means, width, yerr=stds, capsize=5,
               label=behavior_labels[i], alpha=0.8)

    ax.set_xlabel('Experimental Condition', fontsize=12)
    ax.set_ylabel('Behavioral Frequency (%)', fontsize=12)
    ax.set_title('Condition-Dependent Behavioral Patterns', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(condition_labels, fontsize=11)
    ax.legend(loc='upper left')
    ax.grid(axis='y', alpha=0.3)

    # Ensure y-axis starts at 0
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'condition_comparison.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'condition_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {OUTPUT_DIR / 'condition_comparison.pdf'}")

def plot_worldstate_effects():
    """Create world-state effect size visualization."""
    # Data from the comparative analysis report
    models = ['glm-4p5-air', 'llama-v3p1-8b', 'llama4-maverick',
              'llama4-scout', 'mixtral-8x22b', 'qwen3-235b', 'qwen3-30b']
    effect_sizes = [1.271, 0.889, 0.699, 0.816, 1.225, 1.453, 0.816]

    # Create color map based on effect size
    colors = []
    for d in effect_sizes:
        if d >= 0.8:
            colors.append('#d62728')  # Red for large
        elif d >= 0.5:
            colors.append('#ff7f0e')  # Orange for medium
        else:
            colors.append('#2ca02c')  # Green for small

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(models, effect_sizes, color=colors, alpha=0.7)

    # Add effect size thresholds
    ax.axvline(x=0.2, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax.axvline(x=0.8, color='gray', linestyle='--', alpha=0.5, linewidth=1)

    ax.set_xlabel("Cohen's d (Effect Size)", fontsize=12)
    ax.set_ylabel('Model', fontsize=12)
    ax.set_title('Environmental Complexity Effect Sizes\n(Basic vs Extended Environment)',
                 fontsize=14, fontweight='bold')

    # Add legend for effect size interpretation
    small_patch = mpatches.Patch(color='#2ca02c', alpha=0.7, label='Small (d < 0.5)')
    medium_patch = mpatches.Patch(color='#ff7f0e', alpha=0.7, label='Medium (0.5 ≤ d < 0.8)')
    large_patch = mpatches.Patch(color='#d62728', alpha=0.7, label='Large (d ≥ 0.8)')
    ax.legend(handles=[small_patch, medium_patch, large_patch], loc='lower right')

    # Add value labels
    for i, (model, d) in enumerate(zip(models, effect_sizes)):
        ax.text(d + 0.02, i, f'{d:.3f}', va='center', fontsize=9)

    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'worldstate_effects.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'worldstate_effects.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {OUTPUT_DIR / 'worldstate_effects.pdf'}")

def plot_behavioral_heatmap(model_stats):
    """Create heatmap of behavioral patterns across models."""
    models = sorted([m for m in model_stats.keys() if any(model_stats[m].values())])
    behaviors = ['scheming', 'boundary', 'power', 'deception']
    behavior_labels = ['Scheming', 'Boundary\nTesting', 'Power\nSeeking', 'Deception']

    # Create data matrix
    data = np.zeros((len(models), len(behaviors)))
    for i, model in enumerate(models):
        for j, behavior in enumerate(behaviors):
            if model_stats[model][behavior]:
                data[i, j] = np.mean(model_stats[model][behavior])

    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0)

    # Set ticks
    ax.set_xticks(np.arange(len(behaviors)))
    ax.set_yticks(np.arange(len(models)))
    ax.set_xticklabels(behavior_labels, fontsize=10)
    ax.set_yticklabels(models, fontsize=9)

    # Rotate the tick labels and set alignment
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center", va="top")

    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Frequency (%)', rotation=-90, va="bottom", fontsize=10)

    # Add text annotations
    for i in range(len(models)):
        for j in range(len(behaviors)):
            text = ax.text(j, i, f'{data[i, j]:.1f}',
                          ha="center", va="center",
                          color="black" if data[i, j] < 20 else "white",
                          fontsize=8)

    ax.set_title('Behavioral Pattern Heatmap by Model', fontsize=14, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'behavioral_heatmap.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'behavioral_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {OUTPUT_DIR / 'behavioral_heatmap.pdf'}")

def main():
    print("="*80)
    print("GENERATING FIGURES FOR AUTONOMOUS AI SCHEMING PAPER")
    print("="*80)

    print("\nLoading experiment data...")
    experiments = load_classified_logs()
    print(f"✓ Loaded {len(experiments)} experiments")

    print("\nExtracting behavioral statistics...")
    model_stats, condition_stats, worldstate_stats = extract_behavioral_stats(experiments)

    print("\n" + "="*80)
    print("GENERATING FIGURES...")
    print("="*80)

    plot_model_comparison(model_stats)
    plot_condition_comparison(condition_stats)
    plot_worldstate_effects()
    plot_behavioral_heatmap(model_stats)

    print("\n" + "="*80)
    print(f"✓ ALL FIGURES SAVED TO: {OUTPUT_DIR}/")
    print("="*80)
    print("\nGenerated figures:")
    print("  1. model_comparison.pdf/png - Model-level behavioral frequencies")
    print("  2. condition_comparison.pdf/png - Condition-dependent patterns")
    print("  3. worldstate_effects.pdf/png - Effect sizes for environmental complexity")
    print("  4. behavioral_heatmap.pdf/png - Heatmap of all behavioral patterns")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
