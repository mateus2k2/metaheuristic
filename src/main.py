# https://drive.google.com/drive/folders/1mwwU_0wrtVMkreW51i8hSm1CIfZNOwN0?usp=sharing
# https://www-50.ibm.com/isc/esd/dswdown/home?ticket=Xa.2%2FXb.Z7LJBh8BR1xZjJck7sn5ueTW%2FXc.%2FXd.%2FXf.%2FXg.12933972%2FXi.%2FXY.scholars%2FXZ.baGo_22qO_pU4AZjPOu0s22XkgsU-i1d&partNumber=G0798ML
# python "/mnt/c/Program Files/CPLEX2211/python/setup.py" install
# sudo /bin/bash cplex_studio2211.linux_x86_64.bin

# ------------------------------------------------------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------------------------------------------------------

import load as load
import methods.local_search as local_search
import methods.MILP as MILP

print("Loading instance...")
data = load.load("./data/inputs/sm0.txt")
print(data)

print("Running local search...")
solution = local_search.local_search(data, 100)
print(solution)

print("Running MILP...")
MILP.runMILP(data)

