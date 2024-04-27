from datatypes import Clause


class Parser():
    def __init__(self):
        self.numLits = 0
        self.numClauses = 0
        self.clauses = []

    def parse(self, filename):
        with open(filename, 'r') as file:
            for line in file.readlines():
                if (line.startswith('p')):
                    _, _, num_lits, num_clauses = line.split()
                    self.numLits = int(num_lits)
                    self.numClauses = int(num_clauses)
                elif(line.startswith('c')):
                    pass
                else:
                    clause = Clause()
                    for lit in line.split():
                        clause.addLit(int(lit))

                    # Organize the literals
                    # clause.lits.sort(key=lambda x: x)
                    # clause.lits.sort(key=lambda x: abs(x))

                    # TODO: remove redundant literals

                    self.clauses.append(clause)

        return
                    
 # type: ignore