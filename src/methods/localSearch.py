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

def local_search_best_fit(data, initial_solution, neighborhood_func, max_iterations=1000):
    current_solution = initial_solution
    current_value = evaluate.evaluateList(data, current_solution)

    for iteration in range(max_iterations):
        neighbors = neighborhood_func(current_solution)

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

def local_search_first_fit(data, initial_solution, neighborhood_func, max_iterations=1000):
    current_solution = initial_solution
    current_value = evaluate.evaluateList(data, current_solution)

    for iteration in range(max_iterations):
        neighbors = neighborhood_func(current_solution)

        best_neighbor = None
        best_value = float('inf')

        for neighbor in neighbors:
            value = evaluate.evaluateList(data, neighbor)
            if value < best_value:
                best_value = value
                best_neighbor = neighbor
                break
                
        if best_value < current_value:
            current_solution = best_neighbor
            current_value = best_value
        else:
            break

    return current_solution, current_value

def main(data, initial_paran, neighborhood_func_paran, fit_paran):

    initial_solution = None
    if initial_paran == "constructive":    
        _, _, initial_solution = construtivas.main(data, "max", "LPT", "first_fit")
        flat_list = [item for sublist in initial_solution for item in sublist]
    if initial_paran == "rand":    
        flat_list = list(range(data['numJobs']))
        random.shuffle(list(range(data['numJobs'])))
    initial_solution = flat_list
    
    neighborhood_func = None
    if neighborhood_func_paran == "two_opt": neighborhood_func = neighborhood.two_opt
    if neighborhood_func_paran == "two_swap": neighborhood_func = neighborhood.two_swap
    if neighborhood_func_paran == "insertion": neighborhood_func = neighborhood.insertion
    
    new_solution = None
    if fit_paran == "bestFit": new_solution, _ = local_search_best_fit(data, flat_list, neighborhood_func, 1000000)
    if fit_paran == "firstFit": new_solution, _ = local_search_first_fit(data, flat_list, neighborhood_func, 1000000)
     
    encoded_solution = createPeriodsFromList(data, new_solution)

    return 0, evaluate.evaluate(data, encoded_solution), encoded_solution
