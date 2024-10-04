import json
import matplotlib.pyplot as plt
import statistics
from tabulate import tabulate

def dadosArtigo(avrRPDValues, avrTimeValues):
    avrRPDValues["LSFF"] = [
        29.45,
        35.9,
        22.98,
        19.45,
        30.06,
        22.34,
        18.51,
        21.06,
        15.85,
        17.61,
        17.96,
        13.79,
        15.62,
        13.64
    ]
    avrRPDValues["LSBF"] = [
        30.1,
        35.54,
        22.94,
        19.78,
        30.06,
        22.34,
        18.51,
        21.61,
        15.71,
        17.81,
        18.65,
        15.02,
        16.22,
        14.61
    ]
    avrRPDValues["MIP"] = [
        29.37,
        34.96,
        22.02,
        18.22,
        29.27,
        24.08,
        14.98,
        17.46,
        14.7,
        15.95,
        15.47,
        12.72,
        12.29,
        12.29
    ]
    
    avrRPDValues["MILP"] = [
        41.91,
        42.6,
        26.18,
        21.18,
        31.25,
        23.98,
        19.49,
        21.74,
        16.45,
        18.11,
        19.41,
        19.28,
        22.58,
        21.89
    ]

    avrTimeValues["LSFF"] = [
        0.00,
        0.00,
        0.01,
        0.02,
        0.03,
        0.05,
        0.08,
        0.10,
        0.12,
        0.40,
        0.93,
        1.84,
        2.97,
        9.97
    ]

    avrTimeValues["LSBF"] = [
        0.00,
        0.00,
        0.01,
        0.04,
        0.06,
        0.08,
        0.11,
        0.16,
        0.20,
        0.65,
        1.48,
        3.41,
        4.64,
        4.64
    ]

    avrTimeValues["MIP"] = [
        0.22,
        190.85,
        187.03,
        480.32,
        401.31,
        654.89,
        1311.20,
        1810.69,
        1802.08,
        1801.03,
        1802.14,
        1803.88,
        1807.02,
        1809.50
    ]

    avrTimeValues["MILP"] = [
        0.26,
        3.98,
        109.81,
        1554.83,
        1801.21,
        1801.53,
        1801.25,
        1800.27,
        1800.94,
        1800.89,
        1141.10,
        1455.17,
        1800.15,
        1800.30
    ]
    return avrRPDValues, avrTimeValues

def createPeriodsFromList(data, solution):
    periods = []
    curPeriod = []
    periodTime = data['timeDuration']
    periodResource = data['resourceConstraint']

    for tarefa in solution:
        jobTime = data['processingTimes'][tarefa]
        jobResource = data['resourceConsumption'][tarefa]

        if jobTime <= periodTime and jobResource <= periodResource:
            periodTime -= jobTime
            periodResource -= jobResource
            curPeriod.append(tarefa)
        else:
            periods.append(curPeriod)
            curPeriod = [tarefa]
            periodTime = data['timeDuration'] - jobTime
            periodResource = data['resourceConstraint'] - jobResource

    if curPeriod:
        periods.append(curPeriod)

    return periods

def analysis(input, output, type='rpd', version='avr'):
    with open(input, 'r') as results_file:
        results = json.load(results_file)

    fileSizeClass = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "150", "200", "250", "300"]
    avrRPDValues = {}
    stdRPDValues = {}
    avrTimeValues = {}
    stdTimeValues = {}

    for item in results:
        rpd_values = [item['itemResult'][file]['rpd'] for file in item['itemResult']]
        time_values = [item['itemResult'][file]['meanTime'] for file in item['itemResult']]

        avrRPD = sum(rpd_values) / len(rpd_values)
        stdRPD = statistics.stdev(rpd_values) if len(rpd_values) > 1 else 0
        avrRPDValues.setdefault(item['item']["id"], []).append(avrRPD)
        stdRPDValues.setdefault(item['item']["id"], []).append(stdRPD)

        avrTime = sum(time_values) / len(time_values)
        stdTime = statistics.stdev(time_values) if len(time_values) > 1 else 0
        avrTimeValues.setdefault(item['item']["id"], []).append(avrTime)
        stdTimeValues.setdefault(item['item']["id"], []).append(stdTime)

    # for each keey in avrRPDValues, complete the list with zeros if is not the same size as fileSizeClass
    for key in avrRPDValues:
        if len(avrRPDValues[key]) < len(fileSizeClass):
            avrRPDValues[key] += [0] * (len(fileSizeClass) - len(avrRPDValues[key]))
            stdRPDValues[key] += [0] * (len(fileSizeClass) - len(stdRPDValues[key]))
            avrTimeValues[key] += [0] * (len(fileSizeClass) - len(avrTimeValues[key]))
            stdTimeValues[key] += [0] * (len(fileSizeClass) - len(stdTimeValues[key]))
            
    # ----------------------------------------
    # Dados do artigo
    # ----------------------------------------
    avrRPDValues, avrTimeValues = dadosArtigo(avrRPDValues, avrTimeValues)

    plt.figure(figsize=(10, 6))

    colors = [
        'b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown',
        'pink', 'lime', 'navy', 'teal', 'coral', 'gold', 'darkgreen', 
        'darkred', 'violet', 'gray'
    ]

    if type == 'rpd': 
        for i, key in enumerate(avrRPDValues):
            if version == 'std':
                plt.errorbar(fileSizeClass, avrRPDValues[key], yerr=stdRPDValues[key], label=key, marker='o', linewidth=2, color=colors[i % len(colors)], capsize=5)
            if version == 'avr':
                plt.plot(fileSizeClass, avrRPDValues[key], label=key, marker='o', linewidth=2, color=colors[i % len(colors)])

    if type == 'time': 
        for i, key in enumerate(avrTimeValues):
            if version == 'std':
                plt.errorbar(fileSizeClass, avrTimeValues[key], yerr=stdTimeValues[key], label=key, marker='o', linewidth=2, color=colors[i % len(colors)], capsize=5)
            if version == 'avr':
                plt.plot(fileSizeClass, avrTimeValues[key], label=key, marker='o', linewidth=2, color=colors[i % len(colors)])


    plt.grid(True)
    plt.xlabel('Tamanhos de Instâncias')
    if type == 'rpd': plt.ylabel('RPD (com desvio padrão)')
    if type == 'time': plt.ylabel('Tempo (com desvio padrão)')

    plt.legend()
    if output:
        plt.savefig(output)
    
    plt.show()
    
    # makeTable(type, avrRPDValues, stdRPDValues, avrTimeValues, stdTimeValues, fileSizeClass)

def makeTable(type, avrRPDValues, stdRPDValues, avrTimeValues, stdTimeValues, fileSizeClass):
    # Print the data in table format
    if type == 'rpd':
        print("RPD Values:")
        table_data = []
        for key in avrRPDValues:
            row = [key] + avrRPDValues[key] + stdRPDValues.get(key, [])
            table_data.append(row)
        headers = ['ID'] + fileSizeClass + ['StdDev_' + str(f) for f in fileSizeClass]
        print(tabulate(table_data, headers=headers, tablefmt='grid'))

    if type == 'time':
        print("Time Values:")
        table_data = []
        for key in avrTimeValues:
            row = [key] + avrTimeValues[key] + stdTimeValues.get(key, [])
            table_data.append(row)
        headers = ['ID'] + fileSizeClass + ['StdDev_' + str(f) for f in fileSizeClass]
        print(tabulate(table_data, headers=headers, tablefmt='grid'))