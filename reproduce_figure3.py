import matplotlib.pyplot as plt
import json
from matplotlib.lines import Line2D
import os

# Updated path to data and output
DATA_DIR = "dbpa/exps/SFLLM/4.1-Figure3"
RESULTS_DIR = "results"

print("=== Reproducing Figure 3 Statistics (from existing experiment data) ===")
print(f"Reading data from: {DATA_DIR}")

# Check if result file exists
filename = os.path.join(DATA_DIR, 'cvd_guidelines_results.json')
if not os.path.exists(filename):
    print(f"Error: {filename} not found.")
    exit(1)

# Load the results from the JSON file
with open(filename, 'r') as f:
    results = json.load(f)

# Define the prefixes to include and their order
to_leave = ['Act as a doctor. ', 'Act as a nurse. ', 'Act as a medical practitioner. ', 'Act as a medical supervisor. ',
            'Act as a comedian. ', 'Act as a robot from the future. ', 'Act as a NeurIPS reviewer. ', 'Act as a child. ']

# Filter and sort results
filtered_results = [r for r in results if r['prefix'] in to_leave]
top_group = [r for r in filtered_results if r['prefix'] in to_leave[:4]]
bottom_group = [r for r in filtered_results if r['prefix'] in to_leave[4:]]

top_group.sort(key=lambda x: x['jsd'], reverse=True)
bottom_group.sort(key=lambda x: x['jsd'], reverse=True)

sorted_results = top_group + bottom_group

# Print stats
print("\nStats showing robustness (JSD) and significance (p-value) for different personas:")
print("-" * 60)
print(f"{'Persona':<40} | {'JSD (Effect Size)':<20} | {'p-value':<10}")
print("-" * 60)
for r in sorted_results:
    print(f"{r['prefix'].strip():<40} | {r['jsd']:.6f}{'':<12} | {r['p_value']:.4f}")
print("-" * 60)

# PLOTTING
try:
    # Font sizes
    SMALL_SIZE = 20
    MEDIUM_SIZE = 20
    BIGGER_SIZE = 25

    plt.rc('font', size=SMALL_SIZE)
    plt.rc('axes', titlesize=BIGGER_SIZE)
    plt.rc('axes', labelsize=MEDIUM_SIZE)
    plt.rc('xtick', labelsize=SMALL_SIZE)
    plt.rc('ytick', labelsize=SMALL_SIZE)
    plt.rc('legend', fontsize=SMALL_SIZE)
    plt.rc('figure', titlesize=BIGGER_SIZE)

    # Colors
    SIGNIFICANT_COLOR = '#1f77b4'
    INSIGNIFICANT_COLOR = '#d62728'

    # Extract data
    prefixes = [result['prefix'].replace('Act as ', '').strip().rstrip('.') for result in sorted_results]
    jsds = [result['jsd'] for result in sorted_results]
    p_values = [result['p_value'] for result in sorted_results]

    # Create the plot
    fig, ax = plt.subplots(figsize=(16, 5))

    # Plot horizontal points without error bars
    for i, (jsd, p_value) in enumerate(zip(jsds, p_values)):
        color = SIGNIFICANT_COLOR if p_value < 0.05 else INSIGNIFICANT_COLOR
        ax.plot(jsd, len(prefixes) - 1 - i, 'o', 
                color=color, markersize=14,
                label='Significant' if p_value < 0.05 and i == 0 else ('Not Significant' if p_value >= 0.05 and i == len(top_group) else ''))

    # Customize the plot
    ax.set_yticks(range(len(prefixes) - 1, -1, -1))
    prefixes_title = [x.title() for x in prefixes]
    ax.set_yticklabels(prefixes_title)
    ax.set_xlabel(r'$\omega$', fontsize=MEDIUM_SIZE)
    ax.set_title(r'$\omega$ for various input perturbations', fontsize=BIGGER_SIZE)

    # Adjust y-axis to show all labels
    plt.ylim(-1, len(prefixes))

    # Add p-value annotations
    for i, p_value in enumerate(p_values):
        ax.annotate(f'p = {p_value:.2f}', (max(jsds) * 1.05, len(prefixes) - 1 - i), 
                    xytext=(5, 0), textcoords='offset points', 
                    va='center', fontsize=SMALL_SIZE)

    x_min = 0.1
    x_max = 0.5 
    ax.set_xlim(x_min, x_max)

    # Add dashed line between groups
    line_y = len(prefixes) - len(top_group) - 0.5
    ax.axhline(y=line_y, color='black', linestyle='--', alpha=0.5)

    # Add professionally-looking boxes for labels
    box_props = dict(boxstyle='round,pad=0.5', facecolor='lightgrey', alpha=0.3, edgecolor='none')

    # Medical professions box
    ax.text(0.03, (len(prefixes) + line_y) / 2 + 1, 'Medical\nprofessions', 
            transform=ax.get_yaxis_transform(), ha='left', va='center', 
            bbox=box_props, fontsize=SMALL_SIZE, fontweight='bold')

    # Random professions box
    ax.text(0.03, (line_y - 1) / 2 + 1, 'Random\nprofessions', 
            transform=ax.get_yaxis_transform(), ha='left', va='center', 
            bbox=box_props, fontsize=SMALL_SIZE, fontweight='bold')

    # Remove top and right borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Create custom legend with circles instead of squares
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=INSIGNIFICANT_COLOR, markersize=20, label='Not Significant'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=SIGNIFICANT_COLOR, markersize=20, label='Significant'),

    ]

    # Add legend at the bottom, below omega, without a border
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False)

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Increase bottom margin to accommodate legend
    
    # Save the plot
    output_filename = os.path.join(RESULTS_DIR, 'reproduced_figure3.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to {output_filename}")
except Exception as e:
    print(f"\nError plotting: {e}")
