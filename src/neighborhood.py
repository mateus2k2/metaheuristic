import random
import itertools

def simple(solution):
    neighbors = []
    length = len(solution)

    for i in range(length - 1):
        neighbor = solution[:]
        neighbor[i], neighbor[i + 1] = neighbor[i + 1], neighbor[i]
        neighbors.append(neighbor)
    
    return neighbors

def randonInsertion(solution):
    neighbors = []
    length = len(solution)

    for i in range(length - 1):
        neighbor = solution[:]
        index = random.randint(0, length - 1)
        neighbor.insert(index, neighbor.pop(i))
        neighbors.append(neighbor)
    
    return neighbors

def generate_neighbors(solution):
    neighbors = []
    n = len(solution)
    
    # Generate all neighbors by swapping pairs of elements
    for i in range(n):
        for j in range(i + 1, n):
            # Create a copy of the current solution
            neighbor = solution.copy()
            # Swap elements at index i and j
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            # Add the new neighbor to the list
            neighbors.append(neighbor)
    
    return neighbors

def allPermutations(solution):
    neighbors = list(itertools.permutations(solution))
    return neighbors

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