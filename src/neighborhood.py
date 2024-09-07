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
