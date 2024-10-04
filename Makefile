screan: 
	export DISPLAY="$(grep nameserver /etc/resolv.conf | sed 's/nameserver //'):0"

# --------------------------------------------------
# construtivas
# --------------------------------------------------

runBatchConstrutivas:
	clear && cd src && python3 main.py run --input data/batch_construtivas.json --output data/outputs/results_construtivas.json --prints 1 && cd ..

analysisConstrutivas:
	clear && cd src && python3 main.py analysis --input data/outputs/results_construtivas.json --output data/outputs/rpds.png --type rpd --version avr

constructive:
	clear && cd src && python3 main.py constructive --input data/inputs/sm4.txt --phase1 sum --phase2 LPT --phase3 first_fit --graph

# --------------------------------------------------
# MILP
# --------------------------------------------------

MILP:
	clear && cd src && python3 main.py MILP --input data/inputs/sm4.txt --graph

# --------------------------------------------------
# localSearch
# --------------------------------------------------

runBatchLocalSearch:
	clear && cd src && python3 main.py run --input data/batch_localSearch.json --output data/outputs/results_loalSearchV1_100000.json --prints 1 && cd ..

analysisLocalSearch1RPD:
	clear && cd src && python3 main.py analysis --input data/outputs/results_loalSearchV1_100000.json --output data/outputs/100000_RPD.png --type rpd --version std

analysisLocalSearch2RPD:
	clear && cd src && python3 main.py analysis --input data/outputs/results_loalSearchV1_10000.json --output data/outputs/10000_RPD.png --type rpd --version std

analysisLocalSearch1Time:
	clear && cd src && python3 main.py analysis --input data/outputs/results_loalSearchV1_100000.json --output data/outputs/100000_Time.png --type time --version std

analysisLocalSearch2Time:
	clear && cd src && python3 main.py analysis --input data/outputs/results_loalSearchV1_10000.json --output data/outputs/10000_Time.png --type time --version std

localSearch:
	clear && cd src && python3 main.py localSearch --input data/inputs/sm1.txt --initial constructive --neighborhood two_opt --fit bestFit --maxIterations 10000 --graph

# --------------------------------------------------
# VND
# --------------------------------------------------

runBatchVND:
	clear && cd src && python3 main.py run --input data/batch_VND.json --output data/outputs/results_VND.json --prints 1 && cd ..

VND:
	clear && cd src && python3 main.py VND --input data/inputs/sm1.txt --initial constructive --max_iterations 10000 --iterations_without_improvement 10 --p_max 5 --graph
	
analysisVND:
	clear && cd src && python3 main.py analysis --input data/outputs/results_TESTE.json data/outputs/results_construtivas.json --output data/outputs/TESTE.png --type rpd --version avr