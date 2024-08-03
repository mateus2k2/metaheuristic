def load(fileName):
    data = {}
    with open(fileName, 'r') as file:
        data['numJobs'] = int(file.readline())
        data['numPeriods'] = int(file.readline())
        data['timeDuration'] = int(file.readline())
        data['resourceConstraint'] = int(file.readline())
        data['processingTimes'] = list(map(int, file.readline().split()))
        data['resourceConsumption'] = list(map(int, file.readline().split()))
    return data
