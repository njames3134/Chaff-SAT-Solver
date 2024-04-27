from datatypes import *


class DPLL:
    def __init__(self, parser):
        self.sat = False
        self.numLits = parser.numLits
        self.numClauses = parser.numClauses
        self.clauses = parser.clauses

    def add_clause(self, clause):
        self.clauses.append(clause)

    def backtrack(self): # 
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
    def __init__(self, parser):
        self.sat = False
        self.numLits = parser.numLits # Tracks total number of literals
        self.numClauses = parser.numClauses # Tracks total number of clauses
        self.clauses = parser.clauses # List of all clauses (each is a clause object)
        self.states = [] # Track the assignment state of each literal, 0 = X, -n = F for Xn, n = T for Xn
        self.statesNoMod = [] # Track BCP derived states
        for i in range(self.numLits):
            self.states.append(0)
            self.statesNoMod.append(0)
        self.pos = [] # Track the watchlist index of each clause, initially watching index 0 and 1 for all
        for i in range(self.numClauses):
            self.pos.append([0, 1])

    def add_clause(self, clause):
        self.clauses.append(clause)

    def checkAllSAT(self):
        for i in range(self.numClauses):
            if (self.clauses[i].state != ClauseState.SAT):
                return 0
            
        return 1
    
    def updateSAT(self, lit):
        for j in range(self.numClauses):
            if (self.clauses[j].state != ClauseState.SAT and lit in self.clauses[j].lits):
                self.clauses[j].state = ClauseState.SAT

    def solve(self):
        preProc = 0
        for i in range(self.numClauses): # Preprocessing, Remove unit clauses and assign states accordingly
            if (self.clauses[i].numLits == 1):
                self.states[abs(self.clauses[i].lits[0]) - 1] = self.clauses[i].lits[0] # Assign state
                self.statesNoMod[abs(self.clauses[i].lits[0]) - 1] = 1 # Can't modify that
                self.numClauses -= 1
                self.clauses.pop(i)
                self.pos.pop(i)
                preProc = 1 # Preprocessed, try those first
            
        if (preProc == 0):
            self.states[0] = -1 # Start with X1 = F

        stateArrIdx = 0
        prevState = self.states.copy()
        # Resolve Conflicts
        while True:
            i = 0
            while i < self.numClauses:
                curPos = self.pos[i]
                curState = self.states[stateArrIdx]
                curClause = self.clauses[i]
                if (curPos[0] >= curClause.numLits or curPos[1] >= curClause.numLits):
                    break

                for j in range(self.numLits):
                    curState = self.states[j]
                    if (curPos[0] < curClause.numLits and curState == -curClause.lits[curPos[0]]):
                        curPos[0] = curPos[1]
                        curPos[1] += 1
                    elif (curPos[1] < curClause.numLits and curState == -curClause.lits[curPos[1]]):
                        curPos[1] += 1

                if (curPos[1] == curClause.numLits): # Unit Clause, add new state, break from loop
                    stateArrIdx = abs(curClause.lits[curClause.numLits - 1]) - 1
                    self.states[stateArrIdx] = curClause.lits[curClause.numLits - 1]
                    self.statesNoMod[stateArrIdx] = 1
                    curClause.state = ClauseState.SAT
                    break

                i += 1
                
            if (prevState == self.states):
                break

            prevState = self.states.copy()

            # Try states until fully SAT
            for i in range(self.numLits):
                if (self.statesNoMod[i] != 1):
                    self.states[i] = -(i + 1) # Try Xi = F first
                    self.updateSAT(-i)
                    if (self.checkAllSAT()):
                        return 1
                    self.states[i] = i + 1
                    self.updateSAT(i)
                    if (self.checkAllSAT()):
                        return 1

        return 0
                