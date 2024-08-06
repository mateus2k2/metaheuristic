import json
import statistics
import time
import math

import load as load
import checker as checker

import methods.local_search as local_search
import methods.MILP as MILP

# make run >> ./src/data/logs/exec.log

batch = open('data/batch.json', 'r')
batch = json.load(batch)

for item in batch["queeu"]:
    for i in range(0, item["maxFilesToRunPerClass"]):
        file = batch["fileClasses"][item["fileSizeClass"]][i]
        data = load.load(file)
        results = []    

        print(f"File: {file} | Method: {item['method']}")

        for i in range(0, item["numOfTimesToRun"]):
            runTime, value, solution = 0, 0, []

            start_time = time.perf_counter()
            if item["method"] == "localSearch":
                runTime, value, solution = local_search.local_search(data, item["parans"]["maxIterations"])
            elif item["method"] == "MILP":
                runTime, value, solution = MILP.runMILP(data)
            end_time = time.perf_counter()

            results.append({"value": value, "solution": solution, "time": end_time - start_time})
        
        # sum of processing times of data
        lower_bound = math.ceil(max(sum(data["processingTimes"]) / data["timeDuration"], sum(data["resourceConsumption"]) / data["resourceConstraint"]))

        # Extract the best result solution
        best_result = min(results, key=lambda x: x["value"])
        best_value = best_result["value"]
        best_solution = best_result["solution"]

        # Calculate the mean of the result values
        values = [result["value"] for result in results]
        mean_value = statistics.mean(values)

        # Calculate the mean of the result times
        times = [result["time"] for result in results]
        mean_time = statistics.mean(times)

        rpd = ((mean_value - lower_bound)/lower_bound) * 100

        print(f"Lower bound: {lower_bound}")
        print(f"RPD: {rpd}")
        print(f"Mean time: {mean_time}")
        print(f"Best value: {best_value}")
        print(f"Mean value: {mean_value}")
        print(f"Best solution: {best_solution}")
        checker.main(data, best_solution, graph=True, prints=True)
        print("\n\n")

# data = load.load("./data/inputs/sm1.txt")
# value, solution = local_search.local_search(data, 1000)
# print(value)
# value, solution = MILP.runMILP(data)
# print(value)

# checker.main(data=data, solution=solution, graph=True, prints=False)

