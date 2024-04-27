import argparse
from parser import Parser
from datatypes import *

from solver import CHAFF, DPLL

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="input file")
    parser.add_argument("--solver", help="solver method")

    args = parser.parse_args()

    # Parse input file
    parser = Parser()
    vParser = Parser()

    # Tmp
    args.input = "./Inputs/random_v12c257.cnf"
    args.solver = "chaff"
    parser.parse(args.input)
    vParser.parse(args.input)

    if args.solver == 'chaff':
        print("Running CHAFF solver:")
        solver = CHAFF(parser)
    elif args.solver == 'dpll':
        print("Running DPLL solver:")
        solver = DPLL(parser)
    else:
        print("Invalid solver method")
        exit(0)

    # Run the solver
    resSAT = solver.solve()
    verifySAT = 1
    if (resSAT):
        print("Satisfiable")
        print("Assignments:", solver.states)
    else:
        print("Unsatisfiable")

    # Verify result
    for i in range(vParser.numLits):
        lit = solver.states[i]
        if (lit != 0):
            for j in range(vParser.numClauses):
                if (lit in vParser.clauses[j].lits):
                    vParser.clauses[j].state = ClauseState.SAT

    unsatCt = 0
    unsatIdx = []
    for i in range(vParser.numClauses):
        if (vParser.clauses[i].state != ClauseState.SAT):
            unsatCt += 1
            unsatIdx.append(i)
            verifySAT = 0

    if (verifySAT != resSAT):
        print("Wrong Results")
    else:
        print("Correct Results")

