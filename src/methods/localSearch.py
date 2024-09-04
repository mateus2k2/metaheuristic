import methods.construtivas as construtivas
import neighborhood as neighborhood
import evaluate as evaluate
import random

def createPeriodsFromList(data, solution):
    periods = []
    curPeriod = []
    periodTime = data['timeDuration']
    periodResource = data['resourceConstraint']

    for tarefa in solution:
        jobTime = data['processingTimes'][tarefa]
        jobResource = data['resourceConsumption'][tarefa]

        if jobTime <= periodTime and jobResource <= periodResource:
            periodTime -= jobTime
            periodResource -= jobResource
            curPeriod.append(tarefa)
        else:
            periods.append(curPeriod)
            curPeriod = [tarefa]
            periodTime = data['timeDuration'] - jobTime
            periodResource = data['resourceConstraint'] - jobResource

    if curPeriod:
        periods.append(curPeriod)

    return periods

def local_search(data, initial_solution, max_iterations=1000):
    current_solution = initial_solution
    current_value = evaluate.evaluateList(data, current_solution)

    for iteration in range(max_iterations):
        # print(len(neighbors))
        # print(neighbors)
        print(current_value)
        neighbors = neighborhood.two_opt(current_solution)

        best_neighbor = None
        best_value = float('inf')

        for neighbor in neighbors:
            value = evaluate.evaluateList(data, neighbor)
            if value < best_value:
                best_value = value
                best_neighbor = neighbor
                
        if best_value < current_value:
            current_solution = best_neighbor
            current_value = best_value
        else:
            break

    return current_solution, current_value

def main(data):
    _, _, initial_solution = construtivas.main(data, "max", "LPT", "first_fit")
    # _, _, initial_solution = construtivas.main(data, "avg", "LPT", "best_fit")
    # _, _, initial_solution = construtivas.main(data, "max", "LPT", "best_fit")

    flat_list = [item for sublist in initial_solution for item in sublist]
    # flat_list = list(range(data['numJobs']))
    # random.shuffle(list(range(data['numJobs'])))

    new_solution, _ = local_search(data, flat_list, 1000000)
    encoded_solution = createPeriodsFromList(data, new_solution)
    print('initial_solution', flat_list)
    print('initial_solution_value', evaluate.evaluate(data, initial_solution))
    print('solution_found_value', evaluate.evaluate(data, encoded_solution))
    print()
    print()

    return 0, evaluate.evaluate(data, encoded_solution), encoded_solution

# sm140.txt	
# MELHOR DELE = 27670
# MELHOR MEU = 27693