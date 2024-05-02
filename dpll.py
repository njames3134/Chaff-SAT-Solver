from datatypes import *

class DPLL:
    def __init__(self, parser):
        self.sat = False
        self.numLits = parser.numLits
        self.numClauses = parser.numClauses
        self.clauses = parser.clauses
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

    def update_clause(self, clause):
        for lit in clause.lits:
            if self.assign_list[abs(lit)] is None:
                clause.state = ClauseState.UNRES
                return
            elif (lit > 0 and self.assign_list[abs(lit)]) or (lit < 0 and not self.assign_list[abs(lit)]): 
                clause.state = ClauseState.SAT
                return
            else:
                clause.state = ClauseState.UNSAT
                continue
        return

    def backtrack(self):
        # move up the tree to first lit assigned 1 and assign it 0
        for lit in self.assign_stack[::-1]:
            if (self.assign_list[lit] == 0):
                self.assign_list[lit] = None
            elif (self.assign_list[lit] == 1):
                self.assign_list[lit] = 0
                break
            else:
                return False

        # whole tree is None, cant backtrack anymore
        if self.assign_list[self.assign_stack[0]] is None:
            return False

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

        return True

    def forward(self):
        # find unit clause and assign it
        # none_count = 0
        # for c in self.clauses:
        #     for lit in c.lits:
        #         if self.assign_list[abs(lit)] == None:
        #             none_count += 1
        #             break
        #     if none_count == 1:
        #         self.assign_stack.append(abs(lit))
        #         self.assign_list[abs(lit)] = 1 if lit > 0 else 0
        #         c.state = ClauseState.SAT
        #         print(f"assign: x{lit} = {lit > 0}")
        #         return True

        # if no unit clause, find next None in assign list
        lit = 1
        for lit, val in self.assign_list.items():
            if val is None:
                self.assign_list[lit] = 1
                self.assign_stack.append(lit)
                print(f"assign: x{lit} = True")
                return True
        print("no None lits left")
        return False

    def next_literal(self):
        # Check if SAT
        sat_count = 0
        for c in self.clauses:
            sat_count += (c.state == ClauseState.SAT)
        if sat_count == self.numClauses:
            self.sat = True
            return False

        self.forward()
        for c in self.clauses:
            self.update_clause(c)
            if c.state == ClauseState.UNSAT:
                if not self.backtrack():
                    return False

        # return False
        return True

    def solve(self):
        while self.next_literal():
            pass

        for lit, val in self.assign_list.items():
            if val is None:
                self.assign_list[lit] = 0

        count = 0
        for c in self.clauses:
            self.update_clause(c)
            count += c.state == ClauseState.SAT

        
        if count == self.numClauses:
            self.sat = 1
        else:
            self.sat = 0
        print(self.assign_list)
        return
