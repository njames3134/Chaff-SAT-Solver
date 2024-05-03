import sys
from parser import Parser

from datatypes import *

from dpll import DPLL
from chaff import CHAFF

if __name__ == "__main__":
    # Parse input file
    parser = Parser()
    vParser = Parser()

    # Tmp
    benchmark = sys.argv[1]

    input = f"./{benchmark}"
    solver = "chaff"
    parser.parse(input)
    vParser.parse(input)

    if solver == 'chaff':
        print("Running CHAFF solver:")
        solver = CHAFF(parser)
    elif solver == 'dpll':
        print("Running DPLL solver:")
        solver = DPLL(parser)
    else:
        print("Invalid solver method")
        exit(0)

    # Run the solver
    resSAT = solver.solve()
    verifySAT = 1
    if (solver.sat):
        print("Satisfiable")
    else:
        print("Unsatisfiable")

    # Verify result
    remove_list = []
    for i in range(1, solver.numLits):
        lit = solver.assign_list[i]
        if lit == 1:
            lit = i
        else:
            lit = -i
        if (lit != 0):
            remove_list = []
            for clause in vParser.clauses:
                if (lit in clause.lits):
                    clause.state = ClauseState.SAT
                    remove_list.append(clause)
            for c in remove_list:
                vParser.clauses.remove(c)

    if not vParser.clauses:
        print("SAT")
