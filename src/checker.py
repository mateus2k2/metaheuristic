import matplotlib.pyplot as plt
import evaluate as evaluate

# export DISPLAY=$(route.exe print | grep 0.0.0.0 | head -1 | awk '{print $4}'):0.0

def checkSolution(data, periods):
    print("Num Periods: ", data['numPeriods'])
    print("Periods Used: ", len(periods))

    if len(periods) > data['numPeriods']:
        return False
    
    return True

def createPeriods(data, solution):
    periods = []
    periodTmp = []
    currantPoss = 0
    currantPeriod = 0

    periodTime = data['timeDuration']
    periodResource = data['resourceConstraint']

    for i, tarefa in enumerate(solution):
        jobTime = data['processingTimes'][tarefa]
        jobResource = data['resourceConsumption'][tarefa]

        currantPoss += jobTime
        
        if jobTime <= periodTime and jobResource <= periodResource:
            periodTime -= jobTime
            periodResource -= jobResource
        else:
            periods.append(periodTmp)
            periodTmp = []
            currantPeriod += 1
            currantPoss = 0 + jobTime
            periodTime = data['timeDuration'] - jobTime
            periodResource = data['resourceConstraint'] - jobResource

        periodTmp.append({ 'tarefa': tarefa, 'inicio': currantPoss - data['processingTimes'][tarefa], 'fim': currantPoss })

    periods.append(periodTmp)

    return periods

def plotGraph(data, periods):
    fig, ax = plt.subplots()

    # periods.sort(key=lambda x: sum([data['processingTimes'][i["tarefa"]] for i in x]), reverse=True)

    # ---------------------------------------------------------------------------

    ticks = []
    for i in range(0, data['timeDuration'] * (data['numPeriods']+1), data['timeDuration']):
        ax.axvline(x=i, linestyle='dotted', color='gray', alpha=1)
        ticks.append(i)

    for j, period in enumerate(periods):
        for i, tarefa in enumerate(period):
            x = tarefa['inicio'] + (j * data['timeDuration'])
            y = 1
            bar_size = tarefa['fim'] - tarefa['inicio']
            
            ax.barh(y, width=bar_size, left=x, color='green', alpha=1, edgecolor='black', linewidth=1)
            text_value = f"Tarefa = {tarefa['tarefa']} \n Recurso = {data['resourceConsumption'][tarefa['tarefa']]} \n Tempo = {data['processingTimes'][tarefa['tarefa']]}"
            text_x = x + bar_size / 2
            text_y = 1
            ax.text(text_x, text_y, text_value, ha='center', va='center', color='black', fontsize=8, fontweight='bold')
            

    # add red dotted line in last period and last job
    x = (periods[len(periods)-1][len(periods[len(periods)-1])-1]['fim']) + (data['timeDuration'] * (len(periods)-1))
    ax.axvline(x=x, linestyle='dotted', color='red', alpha=1)
    ticks.append(x)

    # add info in the middle of the graph
    x = (data['numPeriods'] * data['timeDuration']) / 2
    ax.text(x, 4, f"Recurso Por Pediodo = {data['resourceConstraint']}", fontsize=12, ha='center', va='center', color='red')
    ax.text(x, 3, f"Tempo Por Pediodo = {data['timeDuration']}", fontsize=12, ha='center', va='center', color='red')

    ax.set_xticks(ticks)
    ax.set_yticks([])

    ax.set_ylim(-0.5, 4.5)
    plt.show()

def main(data, solution):
    print("Recurso por periodo: ", data['resourceConstraint'])
    print("Tempo por periodo: ", data['timeDuration'])
    print("Evaluation: ", evaluate.evaluate(data, solution))

    periods = createPeriods(data, solution)
    checkSolution(data, periods)
    plotGraph(data, periods)