# Executar

Requer Python e o docplex instalado. Para instalar o docplex
Link para os intaladores do docplex: https://drive.google.com/drive/folders/1mwwU_0wrtVMkreW51i8hSm1CIfZNOwN0?usp=drive_link
Siga as instrucões do instalador para instalar o docplex.
Demais dependencias podem ser instaladas com o comando:

pip install -r requirements.txt

```
python3 main.py -h
```

Saida

```
usage: main.py [-h] {run,analysis} ...

Command-line interface for your Python script.

positional arguments:
  {run,analysis}  Sub-command to run.
    run           Run the main method.
    analysis      Run analysis on the input file.
    constructive  Run the constructive method.
    MILP          Run the MILP method.

options:
  -h, --help      show this help message and exit
```

O arquivo de entrada para o comando run deve ser no formado de exemplo na pasta src/data/batch.json. Os metodos a serem executados devem ser adicionados a lista "queue", sequindo o sequinte formato:

```
{
      "method": "constructive",                                                                                   // Método a ser executado
      "parans": {                                                                                                       
          "phase1": "sum",                                                                                        // "sum", "avg" ou "max" 
          "phase2": "LPT",                                                                                        // "LPT", "A-Sharp" ou "HILO"
          "phase3": "first_fit"                                                                                   // "first_fit", "best_fit"
      },                                                                                                              
      "id": "SFFD",                                                                                               // Identificador único do metodo
      "numOfTimesToRun": 10,                                                                                      // Número de vezes que o método será executado cada instância
      "maxFilesToRunPerClass": 10,                                                                                // Número máximo de arquivos por classe
    "fileSizeClass": ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "110", "120", "130", "140"]    // Classes de tamanho de arquivos a serem executadas
},

{
      "method": "MILP",                                                                                           // Método a ser executado
      "parans": {                                                                                                       
      },                                                                                                              
      "id": "SFFD",                                                                                               // Identificador único do metodo
      "numOfTimesToRun": 10,                                                                                      // Número de vezes que o método será executado cada instância
      "maxFilesToRunPerClass": 10,                                                                                // Número máximo de arquivos por classe
    "fileSizeClass": ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "110", "120", "130", "140"]    // Classes de tamanho de arquivos a serem executadas
}
```

A opcão "run" produz um arquivo de saída que pode ser usado como entrada do comando "analysis" para produzir um grafico de comparação entre os métodos.

O comando "constructive" e "MILP" executa o método com apenas um arquivo de entrada e não produz um arquivo de saída. Esses commandos tambem possuem a opção de "graph" que produz um grafico com a vizualização da solução produzida pelo método.

O arquivo Makefile possui os commandos de teste ja prontos para execução.
