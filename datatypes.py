from enum import Enum

class ClauseState(Enum):
    SAT = "Satisfiable"
    UNSAT = "Unsatisfiable"
    UNRES = "Undetermined"

class Clause():
    def __init__(self):
        self.lits = []
        self.numLits = 0
        self.state = ClauseState.UNRES
        self.watched = [0, 1]
        self.unit = False

    def addLit(self, lit):
        if (lit == 0):
            return
        self.lits.append(lit)
        self.numLits += 1

    def removeLit(self, idx):
        self.lits.pop(idx)
        self.numLits -= 1
