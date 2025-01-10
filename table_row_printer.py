import argparse
import os
import sys
import yaml


def print_extracted_info(yaml_file):
    """
    Reads the given YAML file, extracts information of interest,
    and prints it in a readable format.
    """
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}

    model_name = data.get('model', 'N/A')

    keys_of_interest = [
        "IMDP policy performance on true MDPs (J)",
        "IMDP policy performance on IMDPs (J̃)",
        "RL policy performance on true MDPs (J)",
        "RL policy performance on IMDPs (J̃)",
        "existential guarantee",
        "empirical risk for k = 0",
        "empirical risk for k = 5",
        "empirical risk for k = 10",
        "runtime per 10k trajectories"
    ]

    print(f"=== Results for Model: {model_name} ===")

    # Extract and print each key if it exists
    for key in keys_of_interest:
        if key in data:
            print(f"{key}: {data[key]}")
        else:
            print(f"{key}: [Not found in YAML]")

    print() 


def main():
    parser = argparse.ArgumentParser(
        description="Print YAML info for LUI algorithm in seed folder 1650280571."
    )

    # Option to choose a single case study
    parser.add_argument(
        "-c", "--casestudy",
        type=str,
        help='Which case study to visualize. E.g., "aircraft", "betting", "sav", etc.'
    )

    # Option to run for all case studies
    parser.add_argument(
        "-all",
        action="store_true",
        help="Process all case studies currently available in the results folder."
    )

    args = parser.parse_args()

    # Determine which mode we are in:
    if not args.casestudy and not args.all:
        print("Error: Either --casestudy or -all must be specified.")
        sys.exit(1)
    if args.casestudy and args.all:
        print("Error: Both --casestudy and -all options were provided.")
        sys.exit(1)

    # Example recognized case studies
    case_studies = ["aircraft", "betting", "sav", "chain", "drone", "firewire"]

    # If a single case study is requested, validate it
    if args.casestudy and args.casestudy not in case_studies:
        print(f"Error: Invalid case study {args.casestudy} provided.")
        sys.exit(1)

    # Map case_study string to the actual folder names
    filenames = {
        "aircraft": "AIRCRAFT",
        "betting": "BETTING_GAME_FAVOURABLE",
        "sav": "SAV2",
        "drone": "DRONE",
        "chain": "CHAIN_LARGE_TWO_ACTION",       # if these exist
        "firewire": "FIREWIRE"  # if these exist
    }

    # Decide which case studies to process
    if args.all:
        selected_case_studies = case_studies
    else:
        selected_case_studies = [args.casestudy]

    # Our single seed of interest
    seed_of_interest = "1650280571"
    # We only care about LUI_rpol_tied.yaml
    yaml_filename = "LUI_rpol_tied.yaml"

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Now iterate over selected case studies
    for cs in selected_case_studies:
        if cs not in filenames:
            print(f"Warning: No folder mapping for {cs}. Skipping.")
            continue

        base_path = os.path.join(
            script_dir,
            "PRISM-updmps", "prism", "artifact_eval", "results",
            "basic", filenames[cs], "Robust_Policies_WCC"
        )

        # Check if the base path exists
        if not os.path.isdir(base_path):
            print(f"Warning: Base path {base_path} does not exist. Skipping {cs}.")
            continue

        seed_path = os.path.join(base_path, seed_of_interest)
        if not os.path.isdir(seed_path):
            print(
                f"[Skipping] No folder '{seed_of_interest}' for case study '{cs}'."
            )
            continue

        # Construct the full path of the YAML file
        yaml_file = os.path.join(seed_path, yaml_filename)
        if os.path.exists(yaml_file):
            print_extracted_info(yaml_file)
        else:
            print(f"[Skipping] File not found: {yaml_file}")


if __name__ == "__main__":
    main()