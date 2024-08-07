import evaluate as evaluate
import neighborhood as neighborhood
import math
import random

def initial_solution(data):
    return list(range(0, data['numJobs']))

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    return math.exp((old_cost - new_cost) / temperature)

def simulated_annealing(data, maxIter, initialTemp, coolingRate):
    currentSolution = initial_solution(data)
    currentCost = evaluate.evaluate(data, currentSolution)
    bestSolution = currentSolution[:]
    bestCost = currentCost
    
    temperature = initialTemp
    iter = 0
    
    while temperature > 1e-10 and iter < maxIter:
        iter += 1
        
        # Generate a new solution in the neighborhood
        neighborhoodSolutions = neighborhood.randonInsert(currentSolution)
        newSolution = random.choice(neighborhoodSolutions)
        newCost = evaluate.evaluate(data, newSolution)
        
        # Check if we should accept the new solution
        if acceptance_probability(currentCost, newCost, temperature) > random.random():
            currentSolution = newSolution[:]
            currentCost = newCost
            
            # Update the best solution found so far
            if newCost < bestCost:
                bestSolution = newSolution[:]
                bestCost = newCost
        
        # Decrease the temperature
        temperature *= coolingRate
    
    return 0, bestCost, bestSolution
