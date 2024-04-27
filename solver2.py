from datatypes import *

class Chaff:
    def __init__(self, parser):
        self.sat = False
        self.numLits = parser.numLits # Tracks total number of literals
        self.numClauses = parser.numClauses # Tracks total number of clauses
        self.clauses = parser.clauses # List of all clauses (each is a clause object)
        self.states = [] # Track the assignment state of each literal, -1 = X, 0 = F, 1 = T
        for i in range(self.numLits):
            self.states[i] = -1
        self.pos = [] # Track the watchlist index of each clause, initially watching index 0 and 1 for all
        for i in range(self.numClauses):
            self.pos.append([0, 1])

    def add_clause(self, clause):
        self.clauses.append(clause)

    def solve(self):
        for i in range(self.numClauses): # Preprocessing, Remove unit clauses and assign states accordingly
            if (len(self.clauses[i].lits) == 1):
                self.states[abs(self.clauses[i].lits[0])] = self.clauses[i].lits[0] > 0 # Assign state
                self.numClauses -= 1
                self.clauses.pop(i)
                self.pos.pop(i)

        # Iterate until a conflict is hit
        while (True):
            # Iterate through the clauses to find unit clauses
            for i in range(self.numClauses):
                self.clauses[i].lits[self.pos[i][0]]
