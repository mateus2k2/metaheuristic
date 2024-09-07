
run:
	clear && cd src && python3 main.py run --input data/batch.json --output data/results.json --prints 1 && cd ..

analysisConstrutivas:
	clear && cd src && python3 main.py analysis --input data/results_construtivas.json --output data/outputs/rpds.png --type rpd --version avr

constructive:
	clear && cd src && python3 main.py constructive --input data/inputs/sm4.txt --phase1 sum --phase2 LPT --phase3 first_fit --graph

MILP:
	clear && cd src && python3 main.py MILP --input data/inputs/sm4.txt --graph

localSearch:
	clear && cd src && python3 main.py localSearch --input data/inputs/sm1.txt --initial constructive --neighborhood two_opt --fit bestFit --maxIterations 10000 --graph
