def simple(solution):
    nbrhood = []
    
    for i in range(0, len(solution)):
        for j in range(i+1, len(solution)):
            nbrhood.append(solution[:])
            nbrhood[-1][i], nbrhood[-1][j] = nbrhood[-1][j], nbrhood[-1][i]
    
    return nbrhood
