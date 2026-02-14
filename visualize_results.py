#!/usr/bin/env python3
"""
ODRL Benchmark Visualization
=============================

Generates publication-ready plots from multi-prover evaluation results.

Usage:
    python visualize_results.py              # All plots
    python visualize_results.py --cactus     # Cactus plot only
    python visualize_results.py --heatmap    # Agreement heatmap

Requires: matplotlib (pip install matplotlib)

Output: results/plots/*.{pdf,png}
"""

import csv
import json
import os
import sys
from collections import defaultdict

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("WARNING: matplotlib not installed. Install with: pip install matplotlib")

RESULTS_DIR = "results"
PLOT_DIR = os.path.join(RESULTS_DIR, "plots")

# Publication-quality settings
PROVER_COLORS = {
    "vampire": "#1f77b4",
    "eprover": "#ff7f0e",
    "z3": "#2ca02c",
    "cvc5": "#d62728",
    "iprover": "#9467bd",
    "spass": "#8c564b",
}

PROVER_MARKERS = {
    "vampire": "o",
    "eprover": "s",
    "z3": "^",
    "cvc5": "D",
    "iprover": "v",
    "spass": "P",
}

PROVER_LABELS = {
    "vampire": "Vampire",
    "eprover": "E",
    "z3": "Z3",
    "cvc5": "cvc5",
    "iprover": "iProver",
    "spass": "SPASS",
}


def load_evaluation():
    """Load evaluation.json results."""
    fp = os.path.join(RESULTS_DIR, "evaluation.json")
    if not os.path.exists(fp):
        print(f"ERROR: {fp} not found. Run evaluate_provers.py --run first.")
        return None
    with open(fp) as f:
        return json.load(f)


def cactus_plot(results):
    """
    Cactus plot: standard ATP comparison chart.
    X-axis: number of problems solved
    Y-axis: CPU time (log scale)
    """
    if not HAS_MPL:
        return

    fig, ax = plt.subplots(figsize=(8, 5))

    # Group by prover
    prover_times = defaultdict(list)
    for r in results:
        if r["szs_status"] in ("Theorem", "CounterSatisfiable"):
            prover_times[r["prover"]].append(r["wall_time"])

    for prover in sorted(prover_times.keys()):
        times = sorted(prover_times[prover])
        x = list(range(1, len(times) + 1))
        color = PROVER_COLORS.get(prover, "#333333")
        marker = PROVER_MARKERS.get(prover, "o")
        label = PROVER_LABELS.get(prover, prover)
        ax.plot(x, times, color=color, marker=marker, markersize=3,
                linewidth=1.5, label=f"{label} ({len(times)} solved)")

    ax.set_xlabel("Problems solved", fontsize=12)
    ax.set_ylabel("Wall-clock time (s)", fontsize=12)
    ax.set_yscale("log")
    ax.set_title("ODRL Benchmark Suite — Cactus Plot", fontsize=14)
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(True, alpha=0.3)

    os.makedirs(PLOT_DIR, exist_ok=True)
    fig.savefig(os.path.join(PLOT_DIR, "cactus.pdf"), bbox_inches="tight", dpi=300)
    fig.savefig(os.path.join(PLOT_DIR, "cactus.png"), bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  ✓ Cactus plot saved")


def category_comparison(results, problems_meta):
    """
    Bar chart: solve rate per category per prover.
    """
    if not HAS_MPL:
        return

    # Build category counts
    cat_total = defaultdict(int)
    cat_solved = defaultdict(lambda: defaultdict(int))

    # Get problem categories from summary.csv or from results
    prob_cats = {}
    summary_fp = os.path.join(RESULTS_DIR, "summary.csv")
    if os.path.exists(summary_fp):
        with open(summary_fp) as f:
            reader = csv.DictReader(f)
            for row in reader:
                prob_cats[row["Problem"]] = row["Category"]

    for r in results:
        cat = prob_cats.get(r["problem_id"], "Unknown")
        cat_total[cat]  # touch
        if r["szs_status"] in ("Theorem", "CounterSatisfiable"):
            cat_solved[cat][r["prover"]] += 1

    # Count total per category
    seen = set()
    for r in results:
        key = r["problem_id"]
        if key not in seen:
            cat = prob_cats.get(key, "Unknown")
            cat_total[cat] += 1
            seen.add(key)

    if not cat_total:
        return

    categories = sorted(cat_total.keys())
    provers = sorted(set(r["prover"] for r in results))

    fig, ax = plt.subplots(figsize=(12, 6))
    x = range(len(categories))
    width = 0.8 / len(provers)

    for i, prover in enumerate(provers):
        vals = [cat_solved[cat].get(prover, 0) / max(cat_total[cat], 1) * 100
                for cat in categories]
        color = PROVER_COLORS.get(prover, "#333333")
        label = PROVER_LABELS.get(prover, prover)
        bars = ax.bar([xi + i * width for xi in x], vals, width,
                     color=color, label=label, alpha=0.85)

    ax.set_xlabel("Category", fontsize=12)
    ax.set_ylabel("Solve rate (%)", fontsize=12)
    ax.set_title("ODRL Benchmark — Solve Rate by Category", fontsize=14)
    ax.set_xticks([xi + width * len(provers) / 2 for xi in x])
    ax.set_xticklabels(categories, rotation=45, ha="right", fontsize=9)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 110)
    ax.grid(True, axis="y", alpha=0.3)

    fig.savefig(os.path.join(PLOT_DIR, "category_comparison.pdf"),
                bbox_inches="tight", dpi=300)
    fig.savefig(os.path.join(PLOT_DIR, "category_comparison.png"),
                bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  ✓ Category comparison saved")


def difficulty_histogram(results):
    """
    Histogram of difficulty ratings.
    Shows how many problems fall in each difficulty band.
    """
    if not HAS_MPL:
        return

    diff_fp = os.path.join(RESULTS_DIR, "difficulty.csv")
    if not os.path.exists(diff_fp):
        return

    ratings = []
    with open(diff_fp) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ratings.append(float(row["Rating"]))
            except (ValueError, KeyError):
                pass

    if not ratings:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    bins = [0, 0.01, 0.17, 0.33, 0.50, 0.67, 0.83, 1.01]
    labels = ["0.00\n(trivial)", "0.01-0.17", "0.17-0.33", "0.33-0.50",
              "0.50-0.67", "0.67-0.83", "0.83-1.00\n(hard)"]

    counts, _, patches = ax.hist(ratings, bins=bins, edgecolor="black",
                                  color="#4c72b0", alpha=0.85)

    ax.set_xlabel("Difficulty Rating", fontsize=12)
    ax.set_ylabel("Number of Problems", fontsize=12)
    ax.set_title("ODRL Benchmark — Difficulty Distribution", fontsize=14)
    ax.set_xticks([(bins[i] + bins[i+1])/2 for i in range(len(bins)-1)])
    ax.set_xticklabels(labels, fontsize=9)

    # Annotate counts
    for count, patch in zip(counts, patches):
        if count > 0:
            ax.text(patch.get_x() + patch.get_width()/2, count + 0.5,
                   str(int(count)), ha="center", fontsize=10)

    fig.savefig(os.path.join(PLOT_DIR, "difficulty_histogram.pdf"),
                bbox_inches="tight", dpi=300)
    fig.savefig(os.path.join(PLOT_DIR, "difficulty_histogram.png"),
                bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  ✓ Difficulty histogram saved")


def timing_scatter(results):
    """
    Scatter plot: Prover A time vs Prover B time per problem.
    Log-log scale. Points above diagonal = B faster.
    """
    if not HAS_MPL:
        return

    provers = sorted(set(r["prover"] for r in results))
    if len(provers) < 2:
        return

    # Build timing maps
    times = defaultdict(dict)
    for r in results:
        if r["szs_status"] in ("Theorem", "CounterSatisfiable"):
            times[r["prover"]][r["problem_id"]] = r["wall_time"]

    # Plot pairwise for first two main provers
    p1, p2 = provers[0], provers[1]
    common = set(times[p1].keys()) & set(times[p2].keys())

    if not common:
        return

    fig, ax = plt.subplots(figsize=(6, 6))
    x = [max(times[p1][pid], 0.001) for pid in common]
    y = [max(times[p2][pid], 0.001) for pid in common]

    ax.scatter(x, y, alpha=0.5, s=20, color="#4c72b0")
    lims = [min(min(x), min(y)) * 0.5, max(max(x), max(y)) * 2]
    ax.plot(lims, lims, 'k--', alpha=0.3, linewidth=1)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(f"{PROVER_LABELS.get(p1, p1)} time (s)", fontsize=12)
    ax.set_ylabel(f"{PROVER_LABELS.get(p2, p2)} time (s)", fontsize=12)
    ax.set_title(f"ODRL Benchmark — Timing Comparison", fontsize=14)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)

    fig.savefig(os.path.join(PLOT_DIR, "timing_scatter.pdf"),
                bbox_inches="tight", dpi=300)
    fig.savefig(os.path.join(PLOT_DIR, "timing_scatter.png"),
                bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  ✓ Timing scatter saved")


def generate_latex_table(results):
    """
    Generate LaTeX table for paper inclusion.
    """
    provers = sorted(set(r["prover"] for r in results))
    prover_stats = {}

    for p in provers:
        p_results = [r for r in results if r["prover"] == p]
        solved = [r for r in p_results
                 if r["szs_status"] in ("Theorem", "CounterSatisfiable")]
        times = [r["wall_time"] for r in solved]
        prover_stats[p] = {
            "total": len(p_results),
            "solved": len(solved),
            "avg_time": sum(times) / len(times) if times else 0,
            "max_time": max(times) if times else 0,
            "timeouts": sum(1 for r in p_results if r["szs_status"] == "Timeout"),
        }

    # Generate LaTeX
    lines = []
    lines.append(r"\begin{table}[t]")
    lines.append(r"\centering")
    lines.append(r"\caption{Multi-prover evaluation results on ODRL benchmark suite.}")
    lines.append(r"\label{tab:prover-results}")
    lines.append(r"\small")
    lines.append(r"\begin{tabular}{lrrrr}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Prover} & \textbf{Solved} & \textbf{Avg (s)} & \textbf{Max (s)} & \textbf{Timeout} \\")
    lines.append(r"\midrule")

    for p in provers:
        s = prover_stats[p]
        label = PROVER_LABELS.get(p, p)
        lines.append(f"{label} & {s['solved']}/{s['total']} & "
                     f"{s['avg_time']:.3f} & {s['max_time']:.3f} & "
                     f"{s['timeouts']} \\\\")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    latex = "\n".join(lines)

    with open(os.path.join(RESULTS_DIR, "prover_table.tex"), "w") as f:
        f.write(latex)
    print(f"  ✓ LaTeX table saved to results/prover_table.tex")

    return latex


def main():
    os.makedirs(PLOT_DIR, exist_ok=True)

    results = load_evaluation()
    if not results:
        return

    print(f"Loaded {len(results)} results")
    print(f"Generating visualizations...\n")

    cactus_plot(results)
    category_comparison(results, None)
    difficulty_histogram(results)
    timing_scatter(results)
    latex = generate_latex_table(results)

    print(f"\nAll outputs in {PLOT_DIR}/")
    print(f"\nLaTeX table:\n{latex}")


if __name__ == "__main__":
    main()
