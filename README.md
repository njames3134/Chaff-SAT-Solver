# Chaff-SAT-Solver

This is an implementation of CHAFF SAT solver with VSIDS decision heuristics.  

- The benchmakrs used are located in  `benchmarks/SAT` and `benchmarks/UNSAT` for the different sets of test cases that were used.
- mySAT.py is the main file that calls the `parser.py` file to parse the benchmark cnf file in DIMACS format and either `dpll.py` or `chaff.py` for whichever implementation it is currently running
- `datatypes.py` contains the classes and datatypes for the clauses and their satisfiability that were used throughout the project.

To run a benchmark on chaff, call mySAT.py with the location of the benchmark intending to run, for example:
`python3 mySAT.py benchmarks/SAT/random_v12c257.cnf`
