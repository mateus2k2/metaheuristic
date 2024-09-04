
run:
	clear && cd src && python3 main.py run --input data/batch.json --output data/results.json && cd ..

analysisConstrutivas:
	clear && cd src && python3 main.py analysis --input data/results_construtivas.json

constructive:
	clear && cd src && python3 main.py constructive --input data/inputs/sm4.txt --phase1 sum --phase2 LPT --phase3 first_fit --graph

MILP:
	clear && cd src && python3 main.py MILP --input data/inputs/sm4.txt --graph

localSearch:
	clear && cd src && python3 main.py localSearch --input data/inputs/sm140.txt --graph
