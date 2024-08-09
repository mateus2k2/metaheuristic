import evaluate as evaluate

# ------------------------------------------------------------------------------------------------
# PHASE 1
# ------------------------------------------------------------------------------------------------

def sum_jobs(data):
    jobs = list(range(data['numJobs']))
    jobs.sort(key=lambda job: (data["processingTimes"][job], data["resourceConsumption"][job]))
    return jobs

def avg_jobs(data):
    jobs = list(range(data['numJobs']))
    jobs.sort(key=lambda job: (data["processingTimes"][job], data["resourceConsumption"][job]) / 2)
    return jobs

def max_jobs(data):
    jobs = list(range(data['numJobs']))
    jobs.sort(key=lambda job: max(data["processingTimes"][job], data["resourceConsumption"][job]))
    return jobs

# ------------------------------------------------------------------------------------------------
# PHASE 2 
# ------------------------------------------------------------------------------------------------

def LPT(jobs):
    """
    Sort jobs in non-crescent order based on processing time.
    """
    return jobs[::-1]

def LPD(jobs):
    """
    Sorting the jobs always inserting the largest and the smallest jobs in alternation
    """
    n = len(jobs)
    result = [None] * n
    left, right = 0, n - 1
    toggle = True
    
    for i in range(n):
        if toggle:
            result[right] = jobs[i]
            right -= 1
        else:
            result[left] = jobs[i]
            left += 1
        toggle = not toggle
    
    return [job for job in result if job is not None]

def ASharp(jobs):
    """
    sorting the jobs inserting the largest job in the middle of the sequence
    """
    result = []
    while jobs:
        if jobs:
            result.append(jobs.pop(0))  # Largest remaining job
        if jobs:
            result.append(jobs.pop(-1)) # Smallest remaining job
    return result

# ------------------------------------------------------------------------------------------------
# PHASE 3
# ------------------------------------------------------------------------------------------------

def first_fit(data, jobs):
    numJobs = data['numJobs']
    numPeriods = data['numPeriods']
    timeDuration = data['timeDuration']
    resourceConstraint = data['resourceConstraint']
    processingTimes = data['processingTimes']
    resourceConsumption = data['resourceConsumption']
    
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

def best_fit(data, jobs):
    numJobs = data['numJobs']
    numPeriods = data['numPeriods']
    timeDuration = data['timeDuration']
    resourceConstraint = data['resourceConstraint']
    processingTimes = data['processingTimes']
    resourceConsumption = data['resourceConsumption']
    
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

def main(data, phase1, phase2, phase3):
    jobs = None

    if phase1 == "sum":
        jobs = sum_jobs(data)
    elif phase1 == "avr":
        jobs = avg_jobs(data)
    elif phase1 == "max":
        jobs = max_jobs(data)

    if phase2 == "LPT":
        jobs = LPT(jobs)
    elif phase2 == "LPD":
        jobs = LPD(jobs)
    elif phase2 == "ASharp":
        jobs = ASharp(jobs)
    
    if phase3 == "first_fit":
        return first_fit(data, jobs)
    elif phase3 == "best_fit":
        return best_fit(data, jobs)
    
    return 0, 0, []

