import json
import statistics
import time
# import math
# from scipy import stats
# import numpy as np

import analysis as analysis
import options as options
import load as load
import checker as checker

import methods.MILP as MILP
import methods.construtivas as construtivas
import methods.localSearch as localSearch

# export DISPLAY="$(grep nameserver /etc/resolv.conf | sed 's/nameserver //'):0"

# ------------------------------------------------------------------------------------------------------------------------
# Rodar os métodos
# ------------------------------------------------------------------------------------------------------------------------

def run(input, output, prints=1):
    results = []

    batch = open(input, 'r')
    batch = json.load(batch)

    for item in batch["queue"]:
        print()
        if prints > 0: print(f"Method: {item['method']}")
        
        for l, className in enumerate(item["fileSizeClass"]):
            itemResult = {}
            if prints > 0: print(f"Class: {className} Num: {l+1}/{len(item['fileSizeClass'])}")
            
            for i in range(0, item["maxFilesToRunPerClass"]):
                file = batch["fileClasses"][className][i]
                data = load.load(file)
                fileResults = []
                
                if prints > 0: print(f"\tFile: {file} | Id: {item['id']} | Num: {i+1}/{item['maxFilesToRunPerClass']}")

                for i in range(0, item["numOfTimesToRun"]):
                    runTime, value, solution = 0, 0, []

                    start_time = time.perf_counter()
                    if item["method"] == "MILP":
                        runTime, value, solution = MILP.runMILP(data)
                    elif item["method"] == "constructive":
                        runTime, value, solution = construtivas.main(data, item["parans"]["phase1"], item["parans"]["phase2"], item["parans"]["phase3"])
                    elif item["method"] == "localSearch":
                        runTime, value, solution = localSearch.main(data, item["parans"]["initial"], item["parans"]["neighborhood"], item["parans"]["fit"])
                    end_time = time.perf_counter()
                    
                    fileResults.append({"value": value, "solution": solution, "time": end_time - start_time})
                

                # sum of processing times of data
                lower_bound = sum(data["processingTimes"])

                # Extract the best result solution
                best_result = min(fileResults, key=lambda x: x["value"])
                best_value = best_result["value"]
                best_solution = best_result["solution"]

                # Calculate the mean of the result values
                values = [result["value"] for result in fileResults]
                mean_value = statistics.mean(values)

                # Calculate the mean of the result times
                times = [result["time"] for result in fileResults]
                mean_time = statistics.mean(times)

                rpd = ((mean_value - (lower_bound))/(lower_bound)) * 100
                
                if prints > 2:
                    print("Check: ", len(best_solution) > data['numPeriods'])
                
                if prints > 3:
                    print("-----------------------------------")
                    print(f"Lower bound: {lower_bound}")
                    print(f"RPD: {rpd}")
                    print(f"Mean time: {mean_time}")
                    print(f"Best value: {best_value}")
                    print(f"Mean value: {mean_value}")
                    print(f"Best solution: {best_solution}")
                    checker.main(data, best_solution, graph=False, prints=True)
                    print("-----------------------------------")

                itemResult[file] = {"fileResults": fileResults, "meanValue": mean_value, "meanTime": mean_time, "bestValue": best_value, "bestSolution": best_solution, "rpd": rpd, "lowerBound": lower_bound}

            results.append({"itemResult": itemResult, "item": item})

    resultsFile = open(output, 'w')
    json.dump(results, resultsFile, indent=1, separators=(',', ':'))

# ------------------------------------------------------------------------------------------------------------------------
# Comandos
# ------------------------------------------------------------------------------------------------------------------------

args = options.parse_args()
if args.command == 'run':
    run(args.input, args.output, args.prints)

elif args.command == 'analysis':
    analysis.analysis(args.input, args.output, args.type, args.version)

elif args.command == 'constructive':
    data = load.load(args.input)
    _, _, resulut = construtivas.main(data, args.phase1, args.phase2, args.phase3)
    if args.graph:
        checker.main(data, resulut, graph=True, prints=True)

elif args.command == 'MILP':
    data = load.load(args.input)
    _, _, resulut = MILP.runMILP(data)
    if args.graph:
        checker.main(data, resulut, graph=True, prints=True)

elif args.command == 'localSearch':
    data = load.load(args.input)
    _, _, resulut = localSearch.main(data, args.initial, args.neighborhood, args.fit)
    if args.graph:
        checker.main(data, resulut, graph=True, prints=True)
