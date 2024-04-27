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
                    clause.lits.sort(key=lambda x: x)
                    clause.lits.sort(key=lambda x: abs(x))

                    # De-duplicate
                    litsLen = len(clause.lits)
                    i = 0
                    while i < litsLen - 1:
                        if (clause.lits[i] == clause.lits[i + 1]):
                            clause.removeLit(i + 1)
                            litsLen -= 1
                            i -= 1
                        elif (clause.lits[i] == -clause.lits[i + 1]):
                            clause.removeLit(i + 1)
                            clause.removeLit(i)
                            litsLen -= 2
                            i -= 1
                        i += 1
                        
                    self.clauses.append(clause)

        return
                    
 # type: ignore