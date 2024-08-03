# linear-programing-model

## Comandos

RODAR MODELO COM DADOS DE TESTE
glpsol  --cover --clique --gomory --mir -m src/modelo.mod -o src/out/modelo.out > src/out/modeloTerminal.out

RODAR MODELO COM INSTANCIA REAL DE TESTE
glpsol  --cover --clique --gomory --mir -m src/modelo.mod -o src/out/sm1.out --data src/inputs/sm1.dat >> src/out/sm1Terminal.out

GERAR .DAT
python src/generator.py

GERAR DICT COM ANALISE
python src/dataAnalyser.py

RODAR TODOS OS MODELOS
./src/runAll.bash
