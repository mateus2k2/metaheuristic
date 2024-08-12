import json
import statistics
import time
import math
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


import load as load
import checker as checker

import methods.MILP as MILP
import methods.construtivas as construtivas

# make run >> ./src/data/logs/exec.log
# export DISPLAY=$(route.exe print | grep 0.0.0.0 | head -1 | awk '{print $4}'):0.0

# ------------------------------------------------------------------------------------------------------------------------
# Rodar os métodos
# ------------------------------------------------------------------------------------------------------------------------

def run():
    results = []

    batch = open('data/batch.json', 'r')
    batch = json.load(batch)

    for item in batch["queue"]:
        for className in item["fileSizeClass"]:
            itemResult = {}
            for i in range(0, item["maxFilesToRunPerClass"]):
                file = batch["fileClasses"][className][i]
                data = load.load(file)
                fileResults = []

                print(f"File: {file} | Method: {item['method']} | Id: {item['id']}")

                for i in range(0, item["numOfTimesToRun"]):
                    runTime, value, solution = 0, 0, []

                    start_time = time.perf_counter()
                    if item["method"] == "MILP":
                        runTime, value, solution = MILP.runMILP(data)
                    elif item["method"] == "constructive":
                        runTime, value, solution = construtivas.main(data, item["parans"]["phase1"], item["parans"]["phase2"], item["parans"]["phase3"])
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

                # print(f"Lower bound: {lower_bound}")
                # print(f"RPD: {rpd}")
                # print(f"Mean time: {mean_time}")
                # print(f"Best value: {best_value}")
                # print(f"Mean value: {mean_value}")
                # print(f"Best solution: {best_solution}")
                # checker.main(data, best_solution, graph=False, prints=True)
                # print("\n\n")

                itemResult[file] = {"fileResults": fileResults, "meanValue": mean_value, "meanTime": mean_time, "bestValue": best_value, "bestSolution": best_solution, "rpd": rpd, "lowerBound": lower_bound}

            results.append({"itemResult": itemResult, "item": item})

    resultsFile = open('data/results.json', 'w')
    json.dump(results, resultsFile, indent=1, separators=(',', ':'))

# ------------------------------------------------------------------------------------------------------------------------
# Analisar os resultados
# ------------------------------------------------------------------------------------------------------------------------

def analysis():
    with open('data/results.json', 'r') as results_file:
        results = json.load(results_file)

    fileSizeClass = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "150", "200", "250", "300"]
    avrRPDValues = {}
    avrTimeValues = {}

    for item in results:
        rpd_values = [item['itemResult'][file]['rpd'] for file in item['itemResult']]
        time_values = [item['itemResult'][file]['meanTime'] for file in item['itemResult']]

        avrRPD = sum(rpd_values)/len(rpd_values)
        avrRPDValues.setdefault(item['item']["id"], []).append(avrRPD)

        avrTime = sum(time_values)/len(time_values)
        avrTimeValues.setdefault(item['item']["id"], []).append(avrTime)

    plt.figure(figsize=(10, 6))

    for key in avrRPDValues:
        plt.plot(fileSizeClass, avrRPDValues[key], label=key, marker='o', linewidth=2)
        # plt.plot(fileSizeClass, avrTimeValues[key], label=key, marker='o', linewidth=2)


    plt.grid(True)
    plt.xlabel('Tamanhos de Instâncias')
    plt.ylabel('RPD')
    # plt.ylabel('Tempo de Execução')

    plt.legend()
    # plt.savefig('data/outputs/rpds.png')
    # plt.savefig('data/outputs/times.png')
    
    plt.show()


analysis()
# run()