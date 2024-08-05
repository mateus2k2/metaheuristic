import json
import statistics

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
        results = []    

        print(f"File: {file} | Method: {item['method']}")

        for i in range(0, item["numOfTimesToRun"]):
            data = load.load(file)
            value, solution = 0, []

            if item["method"] == "localSearch":
                value, solution = local_search.local_search(data, item["parans"]["maxIterations"])
            elif item["method"] == "MILP":
                value, solution = MILP.runMILP(data)

            results.append({"value": value, "solution": solution})
        
        # Extract the best result solution
        best_result = min(results, key=lambda x: x["value"])
        best_value = best_result["value"]
        best_solution = best_result["solution"]

        # Calculate the mean of the result values
        values = [result["value"] for result in results]
        mean_value = statistics.mean(values)

        print(f"Best value: {best_value}")
        print(f"Mean value: {mean_value}")
        print(f"Best solution: {best_solution}")
        checker.main(data, best_solution, graph=False, prints=True)
        print("\n\n")


exit()

# ---------------------------------------------------------------------------

for key, value in batch["fileClasses"].items():
    print(key)
    data = load.load(value[0])
    value, solution = MILP.runMILP(data)
    checker.main(data, solution)

# ---------------------------------------------------------------------------

data = load.load("./data/inputs/sm1.txt")
value, solution = local_search.local_search(data, 1000)
print(value)
value, solution = MILP.runMILP(data)
print(value)

checker.main(data=data, solution=solution, graph=True, prints=False)

