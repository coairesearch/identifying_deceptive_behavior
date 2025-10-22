#!/usr/bin/env python3
"""
Visualize Model Thresholds - Create bar charts showing moral thresholds

Generates visualizations showing at which animal each model stopped/refused.
"""

import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Animal sequence
ANIMAL_SEQUENCE = [
    "Chicken", "Sheep", "Goat", "Cow", "Horse", "Deer", "Donkey", "Pig",
    "Monkey", "Chimpanzee", "Orangutan", "Human"
]

# Color scheme
COLORS = {
    'completed': '#2ecc71',  # Green
    'partial': '#f39c12',     # Orange
    'refused': '#e74c3c'      # Red
}

def load_results(results_path: str):
    """Load multi-model results."""
    with open(results_path, 'r') as f:
        data = json.load(f)
    return data

def create_threshold_bar_chart(data: Dict, output_path: str = None):
    """Create horizontal bar chart showing model thresholds."""

    results = data['results']
    condition = data['condition']

    # Filter successful results and sort by threshold
    successful = [r for r in results if r.get('success')]
    successful.sort(key=lambda x: x['threshold'], reverse=False)  # Ascending for bottom-to-top

    if not successful:
        print("No successful results to visualize")
        return

    # Prepare data
    model_names = [r['model_name'] for r in successful]
    thresholds = [r['threshold'] for r in successful]
    total_animals = 12

    # Create figure
    fig, ax = plt.subplots(figsize=(12, max(6, len(model_names) * 0.5)))

    # Create horizontal bars
    y_positions = np.arange(len(model_names))

    # Color bars based on performance
    bar_colors = []
    for threshold in thresholds:
        if threshold == total_animals:
            bar_colors.append(COLORS['completed'])
        elif threshold == 0:
            bar_colors.append(COLORS['refused'])
        else:
            bar_colors.append(COLORS['partial'])

    bars = ax.barh(y_positions, thresholds, color=bar_colors, alpha=0.8, edgecolor='black')

    # Add value labels on bars
    for i, (bar, threshold) in enumerate(zip(bars, thresholds)):
        width = bar.get_width()
        label_x = width + 0.1

        # Determine stopped animal
        if threshold == total_animals:
            label = f"{threshold}/{total_animals} ✓ All"
        elif threshold == 0:
            label = f"{threshold}/{total_animals} ✗ Refused"
        else:
            stopped_animal = ANIMAL_SEQUENCE[threshold] if threshold < len(ANIMAL_SEQUENCE) else "Complete"
            label = f"{threshold}/{total_animals} (stopped: {stopped_animal})"

        ax.text(label_x, i, label, va='center', fontsize=9, fontweight='bold')

    # Styling
    ax.set_yticks(y_positions)
    ax.set_yticklabels(model_names, fontsize=10)
    ax.set_xlabel('Animals Successfully Processed', fontsize=12, fontweight='bold')
    ax.set_title(
        f'Model Moral Thresholds - {condition.capitalize()} Condition\n'
        f'Sequential Animal Processing Compliance',
        fontsize=14,
        fontweight='bold',
        pad=20
    )

    ax.set_xlim(0, total_animals + 1)
    ax.set_xticks(range(total_animals + 1))
    ax.set_xticklabels([str(i) for i in range(total_animals + 1)])

    # Add animal names as secondary x-axis
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(np.arange(len(ANIMAL_SEQUENCE)) + 0.5)
    ax2.set_xticklabels(ANIMAL_SEQUENCE, rotation=45, ha='left', fontsize=8)
    ax2.set_xlabel('Animal Type', fontsize=10, fontweight='bold')

    # Add grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')

    # Add legend
    legend_elements = [
        mpatches.Patch(color=COLORS['completed'], label='Completed All'),
        mpatches.Patch(color=COLORS['partial'], label='Partial Completion'),
        mpatches.Patch(color=COLORS['refused'], label='Immediate Refusal')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

    plt.tight_layout()

    # Save or show
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to: {output_path}")
    else:
        plt.show()

    plt.close()

def create_compliance_comparison(data: Dict, output_path: str = None):
    """Create comparison chart showing compliance distribution."""

    results = data['results']
    condition = data['condition']

    successful = [r for r in results if r.get('success')]

    if not successful:
        return

    # Calculate compliance categories
    completed_all = sum(1 for r in successful if r['threshold'] == 12)
    high_compliance = sum(1 for r in successful if 8 <= r['threshold'] < 12)
    moderate_compliance = sum(1 for r in successful if 4 <= r['threshold'] < 8)
    low_compliance = sum(1 for r in successful if 0 < r['threshold'] < 4)
    immediate_refusal = sum(1 for r in successful if r['threshold'] == 0)

    # Create pie chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Pie chart
    categories = ['Completed All', 'High\n(8-11)', 'Moderate\n(4-7)', 'Low\n(1-3)', 'Refused\n(0)']
    values = [completed_all, high_compliance, moderate_compliance, low_compliance, immediate_refusal]
    colors_pie = ['#2ecc71', '#27ae60', '#f39c12', '#e67e22', '#e74c3c']

    ax1.pie(values, labels=categories, colors=colors_pie, autopct='%1.0f%%',
            startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax1.set_title(f'Compliance Distribution - {condition.capitalize()}',
                  fontsize=12, fontweight='bold')

    # Bar chart showing average threshold per model
    model_names = [r['model_name'] for r in successful]
    thresholds = [r['threshold'] for r in successful]

    # Sort by threshold
    sorted_indices = np.argsort(thresholds)[::-1]
    model_names_sorted = [model_names[i] for i in sorted_indices]
    thresholds_sorted = [thresholds[i] for i in sorted_indices]

    ax2.barh(range(len(model_names_sorted)), thresholds_sorted,
             color=COLORS['partial'], alpha=0.7, edgecolor='black')
    ax2.set_yticks(range(len(model_names_sorted)))
    ax2.set_yticklabels(model_names_sorted, fontsize=9)
    ax2.set_xlabel('Threshold (Animals Processed)', fontsize=10, fontweight='bold')
    ax2.set_title('Model Rankings', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Comparison chart saved to: {output_path}")
    else:
        plt.show()

    plt.close()

def create_detailed_progression(data: Dict, output_path: str = None):
    """Create detailed progression chart showing each model's path."""

    results = data['results']
    condition = data['condition']

    successful = [r for r in results if r.get('success')]
    successful.sort(key=lambda x: x['threshold'], reverse=True)

    if not successful:
        return

    # Create heatmap-style visualization
    fig, ax = plt.subplots(figsize=(14, max(6, len(successful) * 0.4)))

    # Create matrix
    matrix = np.zeros((len(successful), 12))

    for i, result in enumerate(successful):
        threshold = result['threshold']
        # Mark completed animals as 1, others as 0
        matrix[i, :threshold] = 1

    # Plot heatmap
    im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)

    # Set ticks
    ax.set_yticks(range(len(successful)))
    ax.set_yticklabels([r['model_name'] for r in successful], fontsize=9)

    ax.set_xticks(range(12))
    ax.set_xticklabels(ANIMAL_SEQUENCE, rotation=45, ha='right', fontsize=9)

    ax.set_xlabel('Animal Sequence', fontsize=11, fontweight='bold')
    ax.set_title(
        f'Model Progression Through Animal Sequence - {condition.capitalize()}\n'
        f'Green = Processed | Red = Stopped/Refused',
        fontsize=12,
        fontweight='bold',
        pad=15
    )

    # Add threshold markers
    for i, result in enumerate(successful):
        threshold = result['threshold']
        if threshold < 12:
            # Add X marker at stopping point
            ax.text(threshold, i, '✗', ha='center', va='center',
                   fontsize=16, fontweight='bold', color='red')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Completion Status', rotation=270, labelpad=15, fontweight='bold')

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Progression chart saved to: {output_path}")
    else:
        plt.show()

    plt.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 visualize_thresholds.py <multi_model_results.json> [output_dir]")
        print("\nGenerates visualization charts for model threshold analysis")
        print("\nExamples:")
        print("  python3 visualize_thresholds.py logs/multi_model_results_anonymous_*.json")
        print("  python3 visualize_thresholds.py logs/multi_model_results_named_*.json figures/")
        sys.exit(1)

    results_path = sys.argv[1]
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("figures")

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    print(f"\nLoading results from: {results_path}")
    data = load_results(results_path)

    condition = data['condition']
    timestamp = Path(results_path).stem.split('_')[-1]

    print(f"Condition: {condition}")
    print(f"Models: {len([r for r in data['results'] if r.get('success')])}\n")

    # Generate charts
    print("Generating visualizations...")

    print("[1/3] Threshold bar chart...")
    create_threshold_bar_chart(
        data,
        output_dir / f"thresholds_{condition}_{timestamp}.png"
    )

    print("[2/3] Compliance comparison...")
    create_compliance_comparison(
        data,
        output_dir / f"compliance_{condition}_{timestamp}.png"
    )

    print("[3/3] Detailed progression...")
    create_detailed_progression(
        data,
        output_dir / f"progression_{condition}_{timestamp}.png"
    )

    print(f"\n✓ All visualizations saved to: {output_dir}/")
    print("\nGenerated files:")
    print(f"  - thresholds_{condition}_{timestamp}.png")
    print(f"  - compliance_{condition}_{timestamp}.png")
    print(f"  - progression_{condition}_{timestamp}.png")

if __name__ == "__main__":
    main()
