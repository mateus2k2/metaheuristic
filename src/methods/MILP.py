from docplex.mp.model import Model

def solve_model(I, J, p, r, T, R, M):
    mdl = Model(name='Scheduling')

    # Decision variables
    X = mdl.binary_var_matrix(I, J, name='X')  # 1 if task j is processed in period i
    y = mdl.continuous_var_dict(I, name='y', lb=0)  # 1 if period i is used
    w = mdl.binary_var_dict(I, name='w')  # 1 if period i has the maximum idle time
    z = mdl.continuous_var(name='z', lb=0)  # Computes the slack time of the period with the maximum

    # Objective function
    mdl.minimize(T * mdl.sum(y[i] for i in I) - z)

    # Constraints
    mdl.add_constraints(mdl.sum(X[i, j] for i in I) == 1 for j in J)  # Each task is assigned to one period
    mdl.add_constraints(mdl.sum(p[j] * X[i, j] for j in J) <= T for i in I)  # Processing time limit per period
    mdl.add_constraints(mdl.sum(r[j] * X[i, j] for j in J) <= R for i in I)  # Resource limit per period
    mdl.add_constraints(X[i, j] <= y[i] for i in I for j in J)  # Tasks assigned only to used periods
    mdl.add_constraint(mdl.sum(w[i] for i in I) == 1)  # Only one period has the maximum idle time
    mdl.add_constraints(w[i] <= y[i] for i in I)  # Maximum idle time period must be a used period
    mdl.add_constraints(z <= (M * (1 - w[i])) + (T * y[i]) - mdl.sum(p[j] * X[i, j] for j in J) for i in I)  # Calculate maximum idle time

    solution = mdl.solve()

    return solution

def convertSolution(solutionCPLX):
    # Extract the solution values and variable names
    solution_values = []
    var_names = []
    
    for var in solutionCPLX.iter_variables():
        solution_values.append(var.solution_value)
        var_names.append(var.name)

    # Create a dictionary to store the jobs assigned to each period
    periods = {}

    # Iterate through the solution values and variable names
    for name, value in zip(var_names, solution_values):
        if name.startswith('X_') and value > 0.5:  # Only consider assignments with value 1
            # Extract job and period indices from the variable name
            _, j, i = name.split('_')
            i, j = int(i), int(j)
            i = i - 1
            j = j - 1
            
            # Initialize the period list if it doesn't exist
            if j not in periods:
                periods[j] = []
            
            # Assign the job to the period
            periods[j].append(i)

    # convert the periods dictionary to a list of periods
    sorted_periods = [periods[j] for j in sorted(periods.keys())]

    # iterate over the w variables to find the period with the most idle time
    w_values = [int(name.split('_')[1]) - 1 for name, value in zip(var_names, solution_values) if name.startswith('w_') and value > 0.5][0]
    sorted_periods.append(sorted_periods.pop(w_values))

    return [job for period in sorted_periods for job in period]

def runMILP(instance):
    J = list(range(1, instance['numJobs'] + 1))  # number of jobs
    I = list(range(1, instance['numPeriods'] + 1))  # number of periods

    p = {j: instance['processingTimes'][j-1] for j in J}  # processing time
    r = {j: instance['resourceConsumption'][j-1] for j in J}  # resource consumption

    T = instance['timeDuration']  # timeDuration
    R = instance['resourceConstraint']  # resourceConstraint
    M = 1000000

    solutionCPLX = solve_model(I, J, p, r, T, R, M)
    if solutionCPLX: 
        solution = convertSolution(solutionCPLX)
        return 0, solutionCPLX.objective_value, solution

    return 0, -1, []

