
import json
import matplotlib.pyplot as plt

def analysis():
    with open('data/results.json', 'r') as results_file:
        results = json.load(results_file)

    fileSizeClass = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "150", "200", "250", "300"]
    avrRPDValues = {}
    avrTimeValues = {}

    for item in results:
        rpd_values = [item['itemResult'][file]['rpd'] for file in item['itemResult']]
        time_values = [item['itemResult'][file]['meanTime'] for file in item['itemResult']]

        avrRPD = sum(rpd_values) / len(rpd_values)
        avrRPDValues.setdefault(item['item']["id"], []).append(avrRPD)

        avrTime = sum(time_values) / len(time_values)
        avrTimeValues.setdefault(item['item']["id"], []).append(avrTime)

    plt.figure(figsize=(10, 6))

    # Define 20 distinct colors
    colors = [
        'b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown',
        'pink', 'lime', 'navy', 'teal', 'coral', 'gold', 'darkgreen', 
        'darkred', 'violet', 'gray'
    ]

    for i, key in enumerate(avrRPDValues):
        plt.plot(fileSizeClass, avrRPDValues[key], label=key, marker='o', linewidth=2, color=colors[i % len(colors)])
        # plt.plot(fileSizeClass, avrTimeValues[key], label=key, marker='o', linewidth=2, color=colors[i % len(colors)])

    plt.grid(True)
    plt.xlabel('Tamanhos de Instâncias')
    plt.ylabel('RPD')
    # plt.ylabel('Tempo de Execução')

    plt.legend()
    # plt.savefig('data/outputs/rpds.png')
    # plt.savefig('data/outputs/times.png')
    
    plt.show()
