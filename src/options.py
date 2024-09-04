import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Command-line interface for your Python script.")

    subparsers = parser.add_subparsers(dest='command', required=True, help='Sub-command to run.')

    # 'run' command
    run_parser = subparsers.add_parser('run', help='Run the main method.')
    run_parser.add_argument('--input', '-i', required=True, help='Path to the input file.')
    run_parser.add_argument('--output', '-o', required=True, help='Path to the output file.')
    run_parser.add_argument('--prints', '-p', action='store_true', help='Enable prints.')

    # 'analysis' command
    analysis_parser = subparsers.add_parser('analysis', help='Run analysis on the input file.')
    analysis_parser.add_argument('--input', '-i', required=True, help='Path to the input file.')

    # 'constructive' command
    constructive_parser = subparsers.add_parser('constructive', help='Run the constructive method.')
    constructive_parser.add_argument('--graph', '-g', action='store_true', help='Creates a Graph.')
    constructive_parser.add_argument('--input', '-i', required=True, help='Path to the input file.')
    constructive_parser.add_argument('--phase1', '-p1', required=True, choices=['sum', 'avg', 'max'], help='Select the operation for phase 1.')
    constructive_parser.add_argument('--phase2', '-p2', required=True, choices=['LPT', 'A-Sharp', 'HILO'], help='Select the method for phase 2.')
    constructive_parser.add_argument('--phase3', '-p3', required=True, choices=['first_fit', 'best_fit'], help='Select the method for phase 3.')

    MILP_parser = subparsers.add_parser('MILP', help='Run the MILP method.')
    MILP_parser.add_argument('--graph', '-g', action='store_true', help='Creates a Graph.')
    MILP_parser.add_argument('--input', '-i', required=True, help='Path to the input file.')

    localSearch_parser = subparsers.add_parser('localSearch', help='Run the localSearch method.')
    localSearch_parser.add_argument('--graph', '-g', action='store_true', help='Creates a Graph.')
    localSearch_parser.add_argument('--input', '-i', required=True, help='Path to the input file.')

    args = parser.parse_args()

    # Validate file paths
    if args.command in ['run', 'constructive']:
        if not os.path.exists(args.input):
            raise FileNotFoundError(f"The input file '{args.input}' does not exist.")
        if args.command == 'run' and not os.path.exists(os.path.dirname(args.output)):
            raise FileNotFoundError(f"The output directory '{os.path.dirname(args.output)}' does not exist.")

    if args.command == 'analysis':
        if not os.path.exists(args.input):
            raise FileNotFoundError(f"The input file '{args.input}' does not exist.")

    return args


def validateJson(file):
    pass