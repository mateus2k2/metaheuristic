import random
import neighborhood as neighborhood
import methods.construtivas as construtivas
import methods.localSearch as localSearch
import analysis as analysis
import evaluate as evaluate

def shake_solution(current_solution, neighborhood_index, perturbation_attempts):
    perturbation_neighbors = [neighborhood.two_opt_perturbation, neighborhood.two_swap_perturbation, neighborhood.insertion_perturbation]
    return perturbation_neighbors[neighborhood_index-1](current_solution, perturbation_attempts)

def smart_vns(problem_data, initial_solution, neighborhood_operators, max_perturbation_attempts, max_iterations, max_iterations_without_improvement):
    current_solution = initial_solution
    optimal_cost = evaluate.evaluateList(problem_data, current_solution)
    
    iterations = 0
    iterations_without_improvement = 0
    
    while iterations < max_iterations and iterations_without_improvement < max_iterations_without_improvement:
        neighborhood_index = 1
        perturbation_attempts = 1
        while neighborhood_index <= len(neighborhood_operators):
            shaken_solution = shake_solution(current_solution, neighborhood_index, perturbation_attempts)
            local_optimum, local_optimum_cost = localSearch.local_search_best_fit(problem_data, shaken_solution, neighborhood_operators[neighborhood_index-1], max_iterations, max_iterations_without_improvement)
            
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

            # for _ in range(0, 1000000000000000000000):
            #     pass
            
        iterations += 1
        iterations_without_improvement += 1
    
    return current_solution, optimal_cost

def main(problem_data, initialization_method, max_iterations, max_iterations_without_improvement, max_perturbation_attempts):
    try:
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
    except  KeyboardInterrupt:
        print(f"            Interrompido")
        _, _, initial_solution = construtivas.main(problem_data, "max", "LPT", "first_fit")
        return 0, evaluate.evaluate(problem_data, initial_solution), initial_solution
