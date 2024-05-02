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
        none_count = 0
        for c in self.clauses:
            for lit in c.lits:
                if self.assign_list[lit] == None:
                    none_count += 1
            if none_count == 1:
                lit = c.lits.index(None)
                self.assign_stack.append(abs(lit))
                self.assign_list[abs(lit)] = lit
                c.state = ClauseState.SAT
                return

        lit = self.assign_queue.pop()
        self.assign_stack.append(lit)
        self.assign_list[lit] = lit 

        return

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
