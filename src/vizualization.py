import matplotlib.pyplot as plt

# i
numeroMaximoPeriodos = 8
# p
tempoTarefas         = [140,45,132,145,150,30,136,80,3,144]   
# r 
recursoTarefas       = [91,95,60,60,170,102,36,33,160,165] 
# T
tempoMaximoPeriodo   = 188 
# R
recursoPorPeriodo    = 170
# solucao
solucao              = [3,4,6,7,8,7,1,4,5,2]      

# ---------------------------------------------------------------------------

# PLOT
fig, ax = plt.subplots()
solucaoClean = [ [] for _ in range(0, numeroMaximoPeriodos) ] 
for i in range(0, len(solucao)):
    for j in range(0, len(solucao)):
        if solucao[j] == i+1:
            solucaoClean[i].append(j)

# ---------------------------------------------------------------------------

#sort periods by the sum of the tasks inside of it
solucaoClean.sort(key=lambda x: sum([tempoTarefas[i] for i in x]), reverse=True)

# ---------------------------------------------------------------------------

ticks = []
for i in range(0, tempoMaximoPeriodo * (numeroMaximoPeriodos+1), tempoMaximoPeriodo):
    ax.axvline(x=i, linestyle='dotted', color='gray', alpha=1)
    ticks.append(i)


for i, periodo in enumerate(solucaoClean):
    currantPoss = i * tempoMaximoPeriodo
    
    text_x = currantPoss + tempoMaximoPeriodo / 2
    # ax.text(text_x, 0.5, f"p={i+1}", fontsize=12, ha='center', va='center', color='red')
    
    for j, tarefa in enumerate(periodo):
        x = currantPoss
        y = 0
        bar_size = tempoTarefas[tarefa]
        
        ax.barh(y, width=bar_size, left=x, color='green', alpha=1, edgecolor='black', linewidth=1)
        text_value = f"Tarefa = {tarefa+1} \n Recurso = {recursoTarefas[tarefa]} \n Tempo = {tempoTarefas[tarefa]}"
        text_x = x + bar_size / 2
        text_y = 0
        ax.text(text_x, text_y, text_value, ha='center', va='center', color='black', fontsize=8, fontweight='bold')

        currantPoss += tempoTarefas[tarefa]
        
        # if ((j == len(periodo) - 1) and (i == len(solucaoClean) - 1)) or True:
        if ((j == len(periodo) - 1) and (i == len(solucaoClean) - 1)):
            ax.axvline(x=currantPoss, linestyle='dotted', color='red', alpha=0.5)
            ticks.append(currantPoss)
        

x = (numeroMaximoPeriodos * tempoMaximoPeriodo) / 2
ax.text(x, 1, f"Recurso Por Pediodo = {recursoPorPeriodo}", fontsize=12, ha='center', va='center', color='red')

ax.set_xticks(ticks)
ax.set_yticks([])

# ax.set_xlim(750, 940)
ax.set_ylim(-0.5, 4.5)

plt.gca().spines['top'].set_visible(False)
plt.savefig("img.png", transparent=True, dpi=300)
plt.show()