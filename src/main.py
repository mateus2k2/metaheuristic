import json
import statistics
import time
import math

import load as load
import checker as checker

import methods.MILP as MILP
import methods.construtivas as construtivas

# make run >> ./src/data/logs/exec.log

results = []

batch = open('data/batch.json', 'r')
batch = json.load(batch)

for item in batch["queeu"]:
    itemResult = {}
    for i in range(0, item["maxFilesToRunPerClass"]):
        file = batch["fileClasses"][item["fileSizeClass"]][i]
        data = load.load(file)
        fileResults = []    

        print(f"File: {file} | Method: {item['method']}")

        for i in range(0, item["numOfTimesToRun"]):
            runTime, value, solution = 0, 0, []

            start_time = time.perf_counter()
            if item["method"] == "MILP":
                runTime, value, solution = MILP.runMILP(data)
            elif item["method"] == "constructive":
                runTime, value, solution = construtivas.main(data, item["parans"]["phase1"], item["parans"]["phase2"], item["parans"]["phase3"])
            end_time = time.perf_counter()
            
            fileResults.append({"value": value, "solution": solution, "time": end_time - start_time})
        

        lower_bound = math.ceil(max(sum(data["processingTimes"]) / data["timeDuration"], sum(data["resourceConsumption"]) / data["resourceConstraint"]))

        # sum of processing times of data
        processingTimesSum = sum(data["processingTimes"])

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

        rpd = ((mean_value - (processingTimesSum))/(processingTimesSum)) * 100

        print(f"Processing times sum: {processingTimesSum}")
        print(f"Lower bound: {lower_bound}")
        print(f"RPD: {rpd}")
        print(f"Mean time: {mean_time}")
        print(f"Best value: {best_value}")
        print(f"Mean value: {mean_value}")
        print(f"Best solution: {best_solution}")
        checker.main(data, best_solution, graph=True, prints=True)
        print("\n\n")

        itemResult[file] = {"fileResults": fileResults, "meanValue": mean_value, "meanTime": mean_time, "bestValue": best_value, "bestSolution": best_solution, "rpd": rpd, "lowerBound": lower_bound}

    results.append({"itemResult": itemResult, "item": item})    

# data = load.load("./data/inputs/sm70.txt")

# runTime, value, solution = local_search.local_search(data, 1000)
# checker.main(data=data, solution=solution, graph=True, prints=True)
# runTime, value, solution = SA.simulated_annealing(data, 1000, 1000, 0.999)
# checker.main(data=data, solution=solution, graph=True, prints=True)
# runTime, value, solution = construtivas.first_fit(data)
# checker.main(data=data, solution=solution, graph=True, prints=True)
# runTime, value, solution = construtivas.best_fit(data)
# checker.main(data=data, solution=solution, graph=True, prints=True)
# runTime, value, solution = MILP.runMILP(data)
# checker.main(data=data, solution=solution, graph=True, prints=True)




