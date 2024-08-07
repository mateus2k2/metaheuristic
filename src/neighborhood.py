import random

def simple(solution):
    nbrhood = []
    
    for i in range(0, len(solution)):
        for j in range(i+1, len(solution)):
            nbrhood.append(solution[:])
            nbrhood[-1][i], nbrhood[-1][j] = nbrhood[-1][j], nbrhood[-1][i]
    
    return nbrhood

def randonInsert(solution):
    nbrhood = []
    n = len(solution)
    
    for i in range(n):
        new_solution = solution[:]
        element = new_solution.pop(i)
        insert_position = random.randint(0, len(new_solution))
        new_solution.insert(insert_position, element)
        nbrhood.append(new_solution)
    
    return nbrhood