def getRPD(data, solution):
    value = evaluate(data, solution)
    lower_bound = sum(data["processingTimes"])
    rpd = ((value - (lower_bound))/(lower_bound)) * 100
    return rpd

def evaluate(data, solution):
    last_index = len(solution)-1
    makeSpan = data['timeDuration'] * (last_index) 

    for job in solution[last_index]:
        makeSpan += data["processingTimes"][job]

    return makeSpan

def evaluateList(data, solution):
    bigNumber = 10000000
    makeSpan = 0

    currentPeriod = 0
    periodTime = data['timeDuration']
    periodResource = data['resourceConstraint']
    
    for job in solution:
        jobTime = data['processingTimes'][job]
        jobResource = data['resourceConsumption'][job]
        
        if jobTime <= periodTime and jobResource <= periodResource:
            periodTime -= jobTime
            periodResource -= jobResource
        else:
            currentPeriod += 1
            makeSpan += data['timeDuration']
            periodTime = data['timeDuration'] - jobTime
            periodResource = data['resourceConstraint'] - jobResource

    makeSpan += (data['timeDuration'] - periodTime)

    if currentPeriod > data['numPeriods']:
        makeSpan += bigNumber

    return makeSpan

def evaluateListBySum(data, solution):
    return sum(data['processingTimes'][job] for job in solution)