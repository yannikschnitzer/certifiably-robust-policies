import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import time

def generate_plot(relative_path, title, file_types, lower_bound=0.0, upper_bound=1.0):
    # Build base_path by going two directories up from this file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir,'..', relative_path)
    
    # Constants
    linewidth = 2
    colors = ['#1f77b4', 'mediumorchid', '#2ca02c', '#3bafff']  # Blue, Purple, Green, Light Blue

    if len(file_types) == 1:
        colors = ['mediumorchid']  # Only LUI

    # Automatically get all folder names as seeds
    seeds = [
        folder for folder in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, folder)) and folder.isdigit()
    ]
    seeds = sorted(seeds, key=int)  # Sort seeds numerically for consistency

    # Helper function to load CSV files dynamically
    def load_data(base_path, seeds, file_types):
        data = {ftype: [] for ftype in file_types}
        for seed in seeds:
            for ftype in file_types:
                file_path = os.path.join(base_path, str(seed), f"{ftype}.csv")
                if os.path.exists(file_path):
                    data[ftype].append(pd.read_csv(file_path))
        return data

    # Plotting helper functions
    def plot_metric(dfs, label, color, x_key, y_key, linestyle="-", alpha_fill=0.2):
        x_values = dfs[0][x_key]
        y_values = [df[y_key] for df in dfs]
        mean_y = np.mean(y_values, axis=0)
        std_y = np.std(y_values, axis=0) / 6  # example dividing by sqrt(n) or something else

        plt.plot(x_values, mean_y, color=color, linewidth=linewidth, linestyle=linestyle)
        plt.fill_between(x_values, mean_y - std_y, mean_y + std_y, color=color, alpha=alpha_fill)

    def plot_rl(dfs, color, x_key, y_key_perf, y_key_guarantee, alpha_fill=0.2):
        x_values = dfs[0][x_key]
        y_values = [df[y_key_perf] for df in dfs]
        y_values_guarantee = [df[y_key_guarantee] for df in dfs]

        mean_y = np.mean(y_values, axis=0)
        mean_y_guarantee = np.mean(y_values_guarantee, axis=0)
        std_y = np.std(y_values, axis=0) / 6
        std_y_guarantee = np.std(y_values_guarantee, axis=0)

        plt.plot(x_values, mean_y, color=color, linewidth=linewidth)
        plt.plot(x_values, mean_y_guarantee, color=color, linewidth=linewidth, linestyle="--")
        plt.fill_between(x_values, mean_y - std_y, mean_y + std_y, color=color, alpha=alpha_fill)
        plt.fill_between(
            x_values,
            mean_y_guarantee - std_y_guarantee,
            mean_y_guarantee + std_y_guarantee,
            color=color,
            alpha=alpha_fill
        )

    # Load data
    data = load_data(base_path, seeds, file_types)

    # Initialize plot
    plt.figure(figsize=(7, 5))
    plt.xscale('log')

    # Plot Existential Guarantee (constant line) - adjusting reference to 'LUI_rpol_tied' if needed
    if "LUI_rpol_tied" in data and len(data["LUI_rpol_tied"]) > 0:
        plt.plot(
            data["LUI_rpol_tied"][0]["Episode"],
            data["LUI_rpol_tied"][0]["Existential Guarantee"],
            linewidth=3, linestyle=":", color="crimson",
            label="Existential Guarantee on true MDPs", alpha=0.8
        )
    elif "LUI_rpol_naive" in data and len(data["LUI_rpol_naive"]) > 0:
        plt.plot(
            data["LUI_rpol_naive"][0]["Episode"],
            data["LUI_rpol_naive"][0]["Existential Guarantee"],
            linewidth=3, linestyle=":", color="crimson",
            label="Existential Guarantee on true MDPs", alpha=0.8
        )

    # Plot other datasets
    for ftype in file_types:
        if ftype in data and len(data[ftype]) > 0:
            plot_metric(
                data[ftype],
                "Performance",
                colors[file_types.index(ftype)],
                "Episode",
                "Performance of IMDP policy on MDPs"
            )
            plot_metric(
                data[ftype],
                "Guarantee",
                colors[file_types.index(ftype)],
                "Episode",
                "Robust Guarantee on IMDPs",
                linestyle="--"
            )

    # Plot RL-specific metrics (example for "LUI_rpol_tied" if present)
    if "LUI_rpol_tied" in data and len(data["LUI_rpol_tied"]) > 0:
        plot_rl(
            data["LUI_rpol_tied"], '#ff7f0e',
            "Episode",
            " Performance of RL policy on MDPs",
            " Robust Guarantee on IMDPs with RL policy"
        )
    

    # Configure plot
    plt.xlabel('# Trajectories', fontsize=14)
    plt.ylabel(r'$\tilde{J}$', rotation=0, fontsize=14)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid(True, color="lightgray", linestyle="--", linewidth=0.6)
    plt.xlim(1, 1000000)
    plt.ylim(lower_bound, upper_bound)

    # Save the plot
    plt.savefig(f"plot_{title}_{time.time_ns()}.pdf", format="pdf", bbox_inches='tight')
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Plot performances for case studies to reproduce Figure 7.")
    
    # Add the -c/--casestudy option to take a string input
    parser.add_argument(
        "-c", "--casestudy",
        type=str,
        help="Which case study to visualize, choose from \"aircraft\", \"betting\", \"sav\", \"chain\", \"drone\", \"firewire\"."
    )
    
    # Add the -all option
    parser.add_argument(
        "-all",
        action="store_true",
        help="Visualize all case studies currently available in the results folder."
    )
    
    # Add the -optimisations option as a boolean flag
    parser.add_argument(
        "-no_optimizations",
        action="store_true",
        help="Visualize case studies ran without optimizations (parameter-tying)."
    )
    
    args = parser.parse_args()
    
    # Handle inputs
    if args.casestudy:
        casestudy = args.casestudy
        print(f"Case Study provided: {args.casestudy}")
    if args.all:
        all_mode = True
        print("All mode enabled.")
    else:
        all_mode = False
    if args.no_optimizations:
        no_optimizations = True
        print("Optimizations disabled (no parameter-tying).")
    else:
        no_optimizations = False

    # Handle invalid or conflicting inputs
    if not args.casestudy and not args.all:
        print("Error: Either --casestudy or -all must be specified.")
        return
    if args.casestudy and args.all:
        print("Error: Both --casestudy and -all options were provided.")
        return
    
    # Example of recognized case studies
    case_studies = ["aircraft", "betting", "sav", "chain", "drone", "firewire"]
    if not all_mode:
        if casestudy not in case_studies:
            print("Error: Invalid case study provided.")
            return

    # Depending on no_optimizations flag
    if no_optimizations:
        file_types = [
            "PAC_rpol_naive", "LUI_rpol_naive", "MAP_rpol_naive", "UCRL_rpol_naive"
        ]
    else:
        file_types = [
            "PAC_rpol_tied", "LUI_rpol_tied", "MAP_rpol_tied", "UCRL_rpol_tied"
        ]

    file_type_single = ["LUI_rpol_tied"]

    lower_bounds = {
        "aircraft": 0.0,
        "betting": 0.0,
        "sav": -0.05,
        "drone": 0.0,
        "chain": 0.0,
        "firewire": 0.0
    }
    upper_bounds = {
        "aircraft": 0.65,
        "betting": 34.9,
        "sav": 0.84,
        "drone": 0.8,
        "chain": 1200.0,
        "firewire": 1.0
    }

    # Map case_study string to directory names below the PRISM-upmdps directory
    filenames = {
        "aircraft": "AIRCRAFT",
        "betting": "BETTING_GAME_FAVOURABLE",
        "sav": "SAV2",
        "drone": "DRONE",
        "chain": "CHAIN_LARGE_TWO_ACTION",
        "firewire": "FIREWIRE"
    }

    # Example usage: we assume `relative_path` is something like:
    # "PRISM-upmdps/prism/artifact_eval/results/basic/AIRCRAFT/Robust_Policies_WCC/"
    # which is 2 levels down from the script directory
    if all_mode:
        for cs in case_studies:
            # Because not all are in 'filenames' dict, you might need checks
            if cs in filenames:
                rel_path = os.path.join(
                    "PRISM-updmps", "prism", "artifact_eval", "results", 
                    "basic", filenames[cs], "Robust_Policies_WCC"
                )
                if not no_optimizations:
                    generate_plot(rel_path, cs, file_type_single, lower_bounds.get(cs, 0.0), upper_bounds.get(cs, 1.0))
                generate_plot(rel_path, cs, file_types, lower_bounds.get(cs, 0.0), upper_bounds.get(cs, 1.0))
    else:
        rel_path = os.path.join(
            "PRISM-updmps", "prism", "artifact_eval", "results",
            "basic", filenames[casestudy], "Robust_Policies_WCC"
        )
        if not no_optimizations:
            generate_plot(rel_path, casestudy, file_type_single, lower_bounds.get(casestudy, 0.0), upper_bounds.get(casestudy, 1.0))
        generate_plot(rel_path, casestudy, file_types, lower_bounds.get(casestudy, 0.0), upper_bounds.get(casestudy, 1.0))


if __name__ == "__main__":
    main()