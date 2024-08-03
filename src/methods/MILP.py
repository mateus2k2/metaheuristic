import cplex
from cplex.exceptions import CplexError

def set_constraints_and_objective(cpx, I, J, p, r, T, R, M):
    # Variable declarations
    var_names = [f'X_{i}_{j}' for i in I for j in J] + [f'y_{i}' for i in I] + [f'w_{i}' for i in I] + ['z']
    var_types = [cpx.variables.type.binary] * (len(I) * len(J) + len(I) * 2) + [cpx.variables.type.continuous]
    cpx.variables.add(names=var_names, types=var_types, lb=[0] * len(var_names))
    
    # Objective function
    objective = [T if 'y' in name else 0 for name in var_names[:-1]] + [-1]
    cpx.objective.set_sense(cpx.objective.sense.minimize)
    cpx.objective.set_linear(list(zip(var_names, objective)))
    
    # Constraints
    rows = []
    senses = []
    rhs = []
    
    # designicaoTarefas
    for j in J:
        row = [[f'X_{i}_{j}' for i in I], [1] * len(I)]
        rows.append(row)
        senses.append('E')
        rhs.append(1)
    
    # limiteDeTempo
    for i in I:
        row = [[f'X_{i}_{j}' for j in J], [p[j] for j in J]]
        rows.append(row)
        senses.append('L')
        rhs.append(T)
    
    # limiteDeRecurso
    for i in I:
        row = [[f'X_{i}_{j}' for j in J], [r[j] for j in J]]
        rows.append(row)
        senses.append('L')
        rhs.append(R)
    
    # limitaTarefasParaPeriodoUsados
    for i in I:
        for j in J:
            row = [[f'X_{i}_{j}', f'y_{i}'], [1, -1]]
            rows.append(row)
            senses.append('L')
            rhs.append(0)
    
    # apenasUmPeriodoComMaiorTempoOcioso
    row = [[f'w_{i}' for i in I], [1] * len(I)]
    rows.append(row)
    senses.append('E')
    rhs.append(1)
    
    # limitaPeriodoComMaiorTempoOciosoParaPeriodosUsados
    for i in I:
        row = [[f'w_{i}', f'y_{i}'], [1, -1]]
        rows.append(row)
        senses.append('L')
        rhs.append(0)
    
    # calculaMaiorTempoOcioso
    for i in I:
        row = [[f'z', f'w_{i}', f'y_{i}'] + [f'X_{i}_{j}' for j in J], [1, -M, T] + [-p[j] for j in J]]
        rows.append(row)
        senses.append('L')
        rhs.append(0)
    
    # Adding constraints to the model
    cpx.linear_constraints.add(lin_expr=rows, senses=senses, rhs=rhs)

def solve_model(I, J, p, r, T, R, M):
    cpx = cplex.Cplex()
    
    try:
        set_constraints_and_objective(cpx, I, J, p, r, T, R, M)
        cpx.solve()
    except CplexError as exc:
        print(exc)
        return
    
    # Results
    solution_values = cpx.solution.get_values()
    var_names = cpx.variables.get_names()
    for name, value in zip(var_names, solution_values):
        print(f"{name} = {value}")

def runMILP(instance):
    J = list(range(1, instance['numJobs'] + 1))  # number of jobs
    I = list(range(1, instance['numPeriods'] + 1))  # number of periods

    p = {j: instance['processingTimes'][j-1] for j in J}  # processing time
    r = {j: instance['resourceConsumption'][j-1] for j in J}  # resource consumption

    T = instance['timeDuration']  # timeDuration
    R = instance['resourceConstraint']  # resourceConstraint
    M = 1000000

    solve_model(I, J, p, r, T, R, M)