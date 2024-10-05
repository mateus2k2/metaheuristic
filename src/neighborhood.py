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
    new_solution = solution[:]
    for _ in range(perturbation_degree):
        pos1, pos2 = sorted(random.sample(range(len(new_solution)), 2))
        new_solution = new_solution[:pos1] + new_solution[pos1:pos2+1][::-1] + new_solution[pos2+1:]
    return new_solution

def two_swap_perturbation(solution, perturbation_degree):
    new_solution = solution[:]
    for _ in range(perturbation_degree):
        pos1, pos2 = random.sample(range(len(new_solution)), 2)
        new_solution[pos1], new_solution[pos2] = new_solution[pos2], new_solution[pos1]
    
    return new_solution

def insertion_perturbation(solution, perturbation_degree):
    new_solution = solution[:]
    for _ in range(perturbation_degree):
        pos1, pos2 = random.sample(range(len(new_solution)), 2)
        element = new_solution[pos1]
        new_solution = new_solution[:pos1] + new_solution[pos1+1:]
        new_solution.insert(pos2, element)
    return new_solution

# simple vertion
def two_opt_simple(solution):
    pos1, pos2 = sorted(random.sample(range(len(solution)), 2))
    new_solution = solution[:pos1] + solution[pos1:pos2+1][::-1] + solution[pos2+1:]
    return new_solution

def two_swap_simple(solution):
    pos1, pos2 = random.sample(range(len(solution)), 2)
    new_solution = solution[:]
    new_solution[pos1], new_solution[pos2] = new_solution[pos2], new_solution[pos1]
    return new_solution

def insertion_simple(solution):
    pos1, pos2 = random.sample(range(len(solution)), 2)
    element = solution[pos1]
    new_solution = solution[:pos1] + solution[pos1+1:]
    new_solution.insert(pos2, element)
    return new_solution