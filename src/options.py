import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Command-line interface for your Python script.")

    subparsers = parser.add_subparsers(dest='command', required=True, help='Sub-command to run.')

    run_parser = subparsers.add_parser('run', help='Run the main method.')
    run_parser.add_argument('--input', '-i', required=True, help='Path to the input file.')
    run_parser.add_argument('--output', '-o', required=True, help='Path to the output file.')
    run_parser.add_argument('--prints', '-p', type=int, choices=[1, 2, 3], help='Set the print level (1, 2, or 3).')

    analysis_parser = subparsers.add_parser('analysis', help='Run analysis on the input file.')
    analysis_parser.add_argument('--input', '-i', required=True, help='Path to the input file.')
    analysis_parser.add_argument('--output', '-o', help='Path to save the graph img.')
    analysis_parser.add_argument('--type', '-t', choices=['rpd', 'time'], required=True, help='Type of the graph to plot.')
    analysis_parser.add_argument('--version', '-v', choices=['avr', 'std'], required=True, help='Version of the graph to plot.')

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
    localSearch_parser.add_argument('--initial', '-l', required=True, choices=['constructive', 'rand'], help='Initial Solution for the local search')
    localSearch_parser.add_argument('--neighborhood', '-n', required=True, choices=['two_opt', 'two_swap', 'insertion'], help='Neighborhood function for the local seach')
    localSearch_parser.add_argument('--fit', '-f', required=True, choices=['bestFit', 'firstFit'], help='Fit function for the local seach')
    localSearch_parser.add_argument('--maxIterations', '-m', type=int, required=True, help='Max iterations for the local seach')
    
    vnd_parser = subparsers.add_parser('VND', help='Run the VND method.')
    vnd_parser.add_argument('--graph', '-g', action='store_true', help='Creates a Graph.')
    vnd_parser.add_argument('--obj', '-f', action='store_true', help='Creates a Graph.')
    vnd_parser.add_argument('--time', '-t', action='store_true', help='Creates a Graph.')
    vnd_parser.add_argument('--input', '-i', required=True, help='Path to the input file.')
    vnd_parser.add_argument('--initial', '-l', required=True, choices=['constructive', 'rand'], help='Initial Solution for the VND')
    vnd_parser.add_argument('--max_iterations', '-m', type=int, required=True, help='Max iterations for VND')
    vnd_parser.add_argument('--iterations_without_improvement', '-mw', type=int, required=True, help='Max Iterations without improvement for VND')
    vnd_parser.add_argument('--p_max', '-p', required=True, type=int, help='P Max for VND')

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

# python3 main.py VND --input data/inputs/sm1.txt --initial constructive --max_iterations 10000 --iterations_without_improvement 10 --p_max 5 --shake random --obj