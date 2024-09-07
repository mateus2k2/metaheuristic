import json
import matplotlib.pyplot as plt
import statistics
from tabulate import tabulate

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
    
    makeTable(type, avrRPDValues, stdRPDValues, avrTimeValues, stdTimeValues, fileSizeClass)

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