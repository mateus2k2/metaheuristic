import random
import neighborhood as neighborhood
import methods.construtivas as construtivas
import analysis as analysis
import evaluate as evaluate

def local_search_vnd(problem_data, current_solution, neighborhood_operator):
    """Perform local search using the given neighborhood operator."""
    optimal_solution = current_solution
    optimal_cost = evaluate.evaluateList(problem_data, current_solution)
    
    improved = True
    while improved:
        new_solution = neighborhood_operator(optimal_solution)[0]
        new_cost = evaluate.evaluateList(problem_data, new_solution)
        
        if new_cost < optimal_cost:
            optimal_solution = new_solution
            optimal_cost = new_cost
        else:
            improved = False
    
    return optimal_solution, optimal_cost

# should take the currant neighborhood in consideration
def shake_solution(current_solution, neighborhood_index, perturbation_attempts):
    """Apply a random perturbation (Shake) to the solution."""
    perturbed_solution = current_solution.copy()
    for _ in range(perturbation_attempts):
        i, j = random.sample(range(len(current_solution)), 2)
        perturbed_solution[i], perturbed_solution[j] = perturbed_solution[j], perturbed_solution[i]
    
    return perturbed_solution

def smart_vns(problem_data, initial_solution, neighborhood_operators, max_perturbation_attempts, max_iterations, max_iterations_without_improvement):
    """Smart VNS algorithm with stopping criteria."""
    current_solution = initial_solution
    optimal_cost = evaluate.evaluateList(problem_data, current_solution)
    
    neighborhood_index = 1
    perturbation_attempts = 1
    iterations = 0
    iterations_without_improvement = 0
    
    while iterations < max_iterations and iterations_without_improvement < max_iterations_without_improvement:
        while neighborhood_index <= len(neighborhood_operators):
            shaken_solution = shake_solution(current_solution, neighborhood_index, perturbation_attempts)
            
            local_optimum, local_optimum_cost = local_search_vnd(problem_data, shaken_solution, neighborhood_operators[neighborhood_index-1])
            
            if local_optimum_cost < optimal_cost:
                current_solution = local_optimum
                optimal_cost = local_optimum_cost
                neighborhood_index = 1
                perturbation_attempts = 1
                iterations_without_improvement = 0
            else:
                if perturbation_attempts >= max_perturbation_attempts:
                    perturbation_attempts = 1
                    neighborhood_index += 1
                else:
                    perturbation_attempts += 1
        
        iterations += 1
        iterations_without_improvement += 1
    
    return current_solution, optimal_cost

def main(problem_data, initialization_method, max_iterations, max_iterations_without_improvement, max_perturbation_attempts):
    
    initial_solution = None
    if initialization_method == "constructive":    
        _, _, initial_solution = construtivas.main(problem_data, "max", "LPT", "first_fit")
        flattened_solution = [item for sublist in initial_solution for item in sublist]
    if initialization_method == "rand":
        flattened_solution = list(range(problem_data['numJobs']))
        random.shuffle(flattened_solution)
    
    initial_solution = flattened_solution
    
    neighborhood_operators = [neighborhood.two_opt, neighborhood.two_swap, neighborhood.insertion]
    
    best_solution, best_cost = smart_vns(problem_data, initial_solution, neighborhood_operators, max_perturbation_attempts, max_iterations, max_iterations_without_improvement)
    
    encoded_solution = analysis.createPeriodsFromList(problem_data, best_solution)
    
    return 0, evaluate.evaluate(problem_data, encoded_solution), encoded_solution

# import random
# import neighborhood as neighborhood
# import methods.construtivas as construtivas
# import analysis as analysis
# import evaluate as evaluate

# def local_search(data, solution, neighborhood_func_index, max_iterations=1000, max_iterations_without_improvement=100):
#     """Perform local search using the given neighborhood function."""
#     neighborhood_functions = [neighborhood.two_opt, neighborhood.two_swap, neighborhood.insertion]
#     neighborhood_function = neighborhood_functions[neighborhood_func_index]
    
#     best_solution = solution
#     best_cost = evaluate.evaluateList(data, solution)
    
#     improved = True
#     while improved:
#         new_solution = neighborhood_function(best_solution)[0]
#         new_cost = evaluate.evaluateList(data, new_solution)
        
#         if new_cost < best_cost:
#             best_solution = new_solution
#             best_cost = new_cost
#         else:
#             improved = False
    
#     return best_solution, best_cost


# def smart_vns(data, initial_solution, neighborhoods, p_max, max_iterations, max_iterations_without_improvement):
#     """Smart VNS algorithm with stopping criteria for max iterations and no improvement."""
#     best_solution = initial_solution
#     best_cost = evaluate.evaluateList(data, best_solution)
    
#     k = 1
#     p = 1
#     iterations = 0
#     iterations_without_improvement = 0
    
#     while iterations < max_iterations/100 and iterations_without_improvement < max_iterations_without_improvement/10:
#         while k <= len(neighborhoods):
#             solution_shake = neighborhoods[k-1](best_solution, p)
#             currant_solution, currant_solution_cost = local_search(data, solution_shake, k-1, max_iterations, max_iterations_without_improvement)
            
#             if currant_solution_cost < best_cost:
#                 best_solution = currant_solution
#                 best_cost = currant_solution_cost
#                 k = 1
#                 p = 1
#                 iterations_without_improvement = 0
#             else:
#                 if p >= p_max:
#                     p = 1
#                     k += 1
#                 else:
#                     p += 1
            
#             iterations += 1
#             iterations_without_improvement += 1
    
#     return best_solution, best_cost

# def main(data, initial_paran, max_iterations, iterations_without_improvement, p_max):
    
#     initial_solution = None
#     if initial_paran == "constructive":    
#         _, _, initial_solution = construtivas.main(data, "max", "LPT", "first_fit")
#         flat_list = [item for sublist in initial_solution for item in sublist]
#     if initial_paran == "rand":
#         flat_list = list(range(data['numJobs']))
#         random.shuffle(flat_list)
#     initial_solution = flat_list
    
#     neighborhoods = [neighborhood.two_opt_perturbation, neighborhood.two_swap_perturbation, neighborhood.insertion_perturbation]
    
#     best_solution, best_cost = smart_vns(data, initial_solution, neighborhoods, p_max, max_iterations, iterations_without_improvement)
    
#     encoded_solution = analysis.createPeriodsFromList(data, best_solution)
    
#     return 0, evaluate.evaluate(data, encoded_solution), encoded_solution
