
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
	clear && cd src && python3 main.py analysis --input data/outputs/results_loalSearchV1_100000.json --output data/outputs/rpds_100000_RPD.png --type rpd --version avr

analysisLocalSearch2RPD:
	clear && cd src && python3 main.py analysis --input data/outputs/results_loalSearchV1_10000.json --output data/outputs/rpds_10000_RPD.png --type rpd --version avr

analysisLocalSearch1Time:
	clear && cd src && python3 main.py analysis --input data/outputs/results_loalSearchV1_100000.json --output data/outputs/rpds_100000_Time.png --type time --version avr

analysisLocalSearch2Time:
	clear && cd src && python3 main.py analysis --input data/outputs/results_loalSearchV1_10000.json --output data/outputs/rpds_10000_Time.png --type time --version avr

localSearch:
	clear && cd src && python3 main.py localSearch --input data/inputs/sm1.txt --initial constructive --neighborhood two_opt --fit bestFit --maxIterations 10000 --graph

