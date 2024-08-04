import load as load
import checker as checker

import methods.local_search as local_search
import methods.MILP as MILP

data = load.load("./data/inputs/sm0.txt")
solution = local_search.local_search(data, 1000)
solution = MILP.runMILP(data)

checker.main(data, solution)

