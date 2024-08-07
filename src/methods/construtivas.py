import evaluate as evaluate

def first_fit(data):
    numJobs = data['numJobs']
    numPeriods = data['numPeriods']
    timeDuration = data['timeDuration']
    resourceConstraint = data['resourceConstraint']
    processingTimes = data['processingTimes']
    resourceConsumption = data['resourceConsumption']
    jobs = list(range(numJobs))
    
    periods = [[] for _ in range(numPeriods)]
    period_time = [0] * numPeriods
    period_resource = [0] * numPeriods

    for job in jobs:
        for i in range(numPeriods):
            if (period_time[i] + processingTimes[job] <= timeDuration and period_resource[i] + resourceConsumption[job] <= resourceConstraint):
                periods[i].append(job)
                period_time[i] += processingTimes[job]
                period_resource[i] += resourceConsumption[job]
                break
        else:
            periods.append([job])
            period_time.append(processingTimes[job])
            period_resource.append(resourceConsumption[job])

    # return the flat periods list
    flatPeriods = [job for period in periods for job in period]
    return 0, evaluate.evaluate(data, flatPeriods), flatPeriods


def best_fit(data):
    numJobs = data['numJobs']
    numPeriods = data['numPeriods']
    timeDuration = data['timeDuration']
    resourceConstraint = data['resourceConstraint']
    processingTimes = data['processingTimes']
    resourceConsumption = data['resourceConsumption']
    jobs = list(range(numJobs))
    
    periods = [[] for _ in range(numPeriods)]
    period_time = [0] * numPeriods
    period_resource = [0] * numPeriods

    for job in jobs:
        best_period = -1
        min_slack = float('inf')

        for i in range(numPeriods):
            if (period_time[i] + processingTimes[job] <= timeDuration and period_resource[i] + resourceConsumption[job] <= resourceConstraint):
                slack = (timeDuration - (period_time[i] + processingTimes[job])) + (resourceConstraint - (period_resource[i] + resourceConsumption[job]))
                if slack < min_slack:
                    min_slack = slack
                    best_period = i

        if best_period == -1:
            periods.append([job])
            period_time.append(processingTimes[job])
            period_resource.append(resourceConsumption[job])
        else:
            periods[best_period].append(job)
            period_time[best_period] += processingTimes[job]
            period_resource[best_period] += resourceConsumption[job]

    flatPeriods = [job for period in periods for job in period]
    return 0, evaluate.evaluate(data, flatPeriods), flatPeriods