import evaluate as evaluate
import neighborhood as neighborhood

def initial_solution(data):
    return list(range(0, data['numJobs']))

def local_search(data, maxIter):
    currentSolution = initial_solution(data)
    bestSolution = currentSolution[:]
    bestCost = evaluate.evaluate(data, bestSolution)
    
    iter = 0
    while iter < maxIter:
        iter += 1
        neighborhoodSolutions = neighborhood.simple(currentSolution)
        
        for solution in neighborhoodSolutions:
            cost = evaluate.evaluate(data, solution)
            
            if cost < bestCost:
                bestSolution = solution[:]
                bestCost = cost
        
        if bestCost < evaluate.evaluate(data, currentSolution):
            currentSolution = bestSolution[:]
        else:
            break
    
    return 0, evaluate.evaluate(data, currentSolution), bestSolution
