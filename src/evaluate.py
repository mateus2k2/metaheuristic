def evaluate(data, solution):
    last_index = len(solution)-1
    makeSpan = data['timeDuration'] * (last_index) 

    for job in solution[last_index]:
        makeSpan += data["processingTimes"][job]

    return makeSpan
        