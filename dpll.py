from datatypes import *


class DPLL:
    def __init__(self, parser):
        self.sat = False
        self.numLits = parser.numLits
        self.numClauses = parser.numClauses
        self.clauses = parser.clauses
        self.assign_queue = [++i for i in range(1, parser.numLits + 1)] # initially order the assign list from 1 to number of lits
        self.assign_list = {}
        self.assign_stack = []

        # generate set of unique lits for assign_list initiallized to None
        lits = set()
        for c in self.clauses:
            for value in iter(c.lits):
                lits.add(abs(value))
        for var in lits:
            self.assign_list[var] = None

    def add_clause(self, clause):
        self.clauses.append(clause)

    def backtrack(self): # 
        # debugging
        self.assign_list[1] = 0
        self.assign_list[2] = 1
        self.assign_stack = [1,2]

        # move up the tree to first lit assigned 1 and assign it 0
        for lit in self.assign_stack[::-1]:
            if (self.assign_list[lit] == 1):
                self.assign_list[lit] = None
            elif (self.assign_list[lit] == 0):
                self.assign_list[lit] = 1
                break
            else: #TODO: This is the case when backtracking on the last variable all the way to root, need to return unsat and end program
                print("Error: got a None assignment during backtrack")

        # update the stack by removing assignments after backtrack
        assign_index = self.assign_stack.index(lit)
        updated_lits = self.assign_stack[assign_index:]
        self.assign_stack = self.assign_stack[:assign_index + 1]

        # reset assignment for everything not in the stack
        self.assign_list = {lit: None if lit not in self.assign_stack else self.assign_list[lit] for lit in self.assign_list}

        # update clause states for clauses that contained changed lits
        for c in self.clauses:
            abs_lits = [abs(literal) for literal in c.lits]
            for lit in updated_lits:
                c.state = ClauseState.UNRES if lit in abs_lits else c.state

        return

    def forward(self):
        # find unit clause and assign it
        for c in self.clauses:
            abs_lits = [abs(literal) for literal in c.lits]
            for lit in abs_lits:
                # find unassigned variable in any clause and assign it
                
                # update assign_stack and assign_list

                pass


        pass

    def next_literal(self):
        # Check if SAT
        sat_count = 0
        for c in self.clauses:
            sat_count += (c.state == ClauseState.SAT)
        if sat_count == self.numClauses:
            self.sat = True
            return False

        self.forward()

        # Backtrack
        self.backtrack

        # Forward

    def solve(self):
        self.backtrack()
        # print(self.assign_queue)
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

    def preprocess(self):
        preProc = 0
        for i in range(self.numClauses): # Preprocessing, Remove unit clauses and assign states accordingly
            if (self.clauses[i].numLits == 1):
                self.states[abs(self.clauses[i].lits[0]) - 1] = self.clauses[i].lits[0] # Assign state
                self.statesNoMod[abs(self.clauses[i].lits[0]) - 1] = 1 # Can't modify that
                self.numClauses -= 1
                self.clauses.pop(i)
                self.pos.pop(i)
                preProc = 1 # Preprocessed, try those first

        return preProc

    def bcp(self): # TODO
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

    def solve(self):
        if (self.preprocess() == 0):
            self.states[0] = -1 # Start with X1 = F

        # Try states until fully SAT
        for i in range(self.numLits):
            self.bcp()
            if (self.statesNoMod[i] == 1):
                self.updateSAT(self.states[i])
                if (self.checkAllSAT()):
                    return 1
            elif (self.statesNoMod[i] != 1):
                self.states[i] = -(i + 1) # Try Xi = F first
                self.updateSAT(-i)
                if (self.checkAllSAT()):
                    return 1
                self.states[i] = i + 1
                self.updateSAT(i)
                if (self.checkAllSAT()):
                    return 1

        return 0
                
