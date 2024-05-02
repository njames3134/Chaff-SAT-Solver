import sys
from parser import Parser

from datatypes import *

from dpll import CHAFF, DPLL

if __name__ == "__main__":
    # Parse input file
    parser = Parser()
    vParser = Parser()

    # Tmp
    benchmark = sys.argv[1]

    input = f"./benchmarks/{benchmark}"
    solver = "dpll"
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
    # verifySAT = 1
    # if (resSAT):
    #     print("Satisfiable")
    #     print("Assignments:", solver.states)
    # else:
    #     print("Unsatisfiable")
    #
    # # Verify result
    # for i in range(vParser.numLits):
    #     lit = solver.states[i]
    #     if (lit != 0):
    #         for j in range(vParser.numClauses):
    #             if (lit in vParser.clauses[j].lits):
    #                 vParser.clauses[j].state = ClauseState.SAT
    #
    # unsatCt = 0
    # unsatIdx = []
    # for i in range(vParser.numClauses):
    #     if (vParser.clauses[i].state != ClauseState.SAT):
    #         unsatCt += 1
    #         unsatIdx.append(i)
    #         verifySAT = 0
    #
    # if (verifySAT != resSAT):
    #     print("Wrong Results")
    # else:
    #     print("Correct Results")

