bigNumber = 100000

def evaluate(data, solution):
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
        