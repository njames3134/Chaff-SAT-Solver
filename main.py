import argparse
from parser import Parser

from solver import CHAFF, DPLL

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="input file")
    parser.add_argument("--solver", help="solver method")

    args = parser.parse_args()

    # Parse input file
    parser = Parser()

    # Tmp
    args.input = "./Inputs/random_v5c5.cnf"
    args.solver = "chaff"
    parser.parse(args.input)

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
    solver.solve()
