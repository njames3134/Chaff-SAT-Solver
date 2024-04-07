from datatypes import *


class DPLL:
    def __init__(self, parser):
        self.sat = False
        self.numLits = parser.numLits
        self.numClauses = parser.numClauses
        self.clauses = parser.clauses

    def add_clause(self, clause):
        self.clauses.append(clause)

    def backtrack(self):
        pass

    def forward(self):
        pass

    def next_literal(self):
        # Check if SAT
        sat_count = 0
        for c in self.clauses:
            sat_count += (c.state == ClauseState.SAT)
        if sat_count == self.numClauses:
            self.sat = True
            return False
        
        # Backtrack

        # Forward

    def solve(self):
        while self.next_literal():
            pass
        pass

class CHAFF:
    def __init__(self):
        pass

    def solve(self):
        pass
