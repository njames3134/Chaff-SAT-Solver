class SolverData():
    def __init__(self, numLits, numClauses):
        self.clauses = []
        self.numLits = numLits
        self.numClauses = numClauses
        self.satStatus = []

        for i in range(numClauses):
            satStatus.append(0)

    def addClause(self, Clause):
        self.clauses.append(Clause)

    def getClause(self, idx):
        return self.clauses[idx]

    def chkSat(self):
        for i in self.satStatus:
            if (i == 0):
                return 0

        return 1


class Clause():
    def __init__(self, numLits):
        self.lits = []

    def addLit(self, lit):
        if (lit == 0):
            raise ValueError('Invalid Literal Value')
        self.lits.append(lit)

    def chkSat(self, lit):
        if (len(self.lits) == 0):
            return 1

        for i in self.lits:
            if (i == lit):
                return 1
        
        return 0