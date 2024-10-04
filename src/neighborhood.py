import random
import itertools

def two_opt(solution):
    neighbors = []

    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            two_opt_neighbor = solution[:i] + solution[i:j+1][::-1] + solution[j+1:]
            neighbors.append(two_opt_neighbor)

    return neighbors

def two_swap(solution):
    neighbors = []

    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            two_swap_neighbor = solution[:]
            two_swap_neighbor[i], two_swap_neighbor[j] = two_swap_neighbor[j], two_swap_neighbor[i]
            neighbors.append(two_swap_neighbor)
    
    return neighbors

def insertion(solution):
    neighbors = []
    
    for i in range(len(solution)):
        for j in range(len(solution)):
            if i != j:
                insertion_neighbor = solution[:]
                element = insertion_neighbor.pop(i)
                insertion_neighbor.insert(j, element)
                neighbors.append(insertion_neighbor)

    return neighbors

# version that return only one neighbor with a degree of perturbation p

def two_opt_perturbation(solution, perturbation_degree):
    n = len(solution)
    pos1 = random.randint(0, n-1)
    max_dist = min(int(perturbation_degree * n), n-1)
    pos2 = (pos1 + random.randint(1, max_dist)) % n
    if pos1 > pos2:
        pos1, pos2 = pos2, pos1
    return solution[:pos1] + solution[pos1:pos2+1][::-1] + solution[pos2+1:]

def two_swap_perturbation(solution, perturbation_degree):
    n = len(solution)
    swaps = max(1, int(perturbation_degree * n)) 
    for _ in range(swaps):
        pos1, pos2 = random.sample(range(n), 2)
        solution[pos1], solution[pos2] = solution[pos2], solution[pos1]
    return solution

def insertion_perturbation(solution, perturbation_degree):
    n = len(solution)
    insertions = max(1, int(perturbation_degree * n)) 
    for _ in range(insertions):
        pos1 = random.randint(0, n-1)
        max_dist = min(int(perturbation_degree * n), n-1)
        pos2 = (pos1 + random.randint(1, max_dist)) % n
        element = solution.pop(pos1)
        solution.insert(pos2, element)
    return solution