from datatypes import *

class CHAFF:
    def __init__(self, parser):
        self.sat = False
        self.numLits = parser.numLits
        self.numClauses = parser.numClauses
        self.clauses = parser.clauses
        self.assign_list = {}
        self.assign_stack = []
        self.bcp_success = 1
        self.implied_lits = []
        self.scores = {}
        self.decay = 0.75

        # generate set of unique lits for assign_list initiallized to None
        lits = set()
        for c in self.clauses:
            for value in iter(c.lits):
                lits.add(abs(value))
        for var in lits:
            self.assign_list[var] = None

        for clause in self.clauses:
            clause.watched = [0, 1]
        
        for lit in range(1, parser.numLits + 1):
            self.scores[lit] = 1

    def add_clause(self, clause):
        self.clauses.append(clause)

    def is_unit(self, clause):
        unsat_count = 0
        for lit in clause.lits:
            if (lit == abs(lit)) == self.assign_list[abs(lit)]:
                continue
            elif self.assign_list[abs(lit)] is not None:
                unsat_count += 1
        return (unsat_count == clause.numLits - 1)

    def move_watched(self, clause, lit):
        idx = clause.lits.index(lit) 
        for i, lit in enumerate(clause.lits):
            if i != clause.watched[0] and i != clause.watched[1] and self.assign_list[abs(lit)] is None:
                clause.watched.remove(idx)
                clause.watched.append(i)
                break
        return

    def update_watched(self, clause):
        # only process a clause if one literal is set to false, ignore true/unassigned       
        clause.is_unit = False

        if clause.state == ClauseState.SAT:
            return

        # get status of the watched literals
        lit1 = clause.lits[clause.watched[0]]
        lit2 = clause.lits[clause.watched[1]]
        if self.assign_list[abs(lit1)] is None:
            val1 = None
        else:
            val1 = self.assign_list[abs(lit1)] == lit1

        if self.assign_list[abs(lit2)] is None:
            val2 = None
        else:
            val2 = self.assign_list[abs(lit2)] == lit2

        # decide how to move watched index
        if val1 is None and val2 is None:
            return
        elif val1 or val2:
            clause.state = ClauseState.SAT
            return
        else:
            if not val1: self.move_watched(clause, lit1)
            if not val2: self.move_watched(clause, lit2)
        
        # get number of unassigned literals in the clause
        none_count = 0
        for lit in clause.lits:
            if self.assign_list[abs(lit)] is None:
                none_count += 1
            elif (lit == abs(lit)) == self.assign_list[abs(lit)]:
                clause.state = ClauseState.SAT
                return

        if clause.state != ClauseState.SAT and none_count == 0:
            clause.state = ClauseState.UNSAT
        elif clause.state != ClauseState.SAT and none_count == 1:
            clause.is_unit = True
        
        return
        
    def preprocess(self):
        # assign all single lit clauses
        implications = set()
        for clause in self.clauses:
            if clause.numLits == 1:
                lit = abs(clause.lits[0])
                self.assign_list[lit] = 1 if lit == clause.lits[0] else 0
                if lit in implications and clause.lits[0] not in implications: # unsat single lit clauses
                    return False
                implications.add(clause.lits[0])
                self.numClauses -= 1
        
        # remove single lit clauses
        self.clauses = [clause for clause in self.clauses if clause.numLits != 1]

        # see if already unsat from unit clauses and find all new sat clauses
        sat_clauses = []
        for clause in self.clauses:
            unsat_count = 0
            for lit in clause.lits:
                if (lit == abs(lit)) == self.assign_list[abs(lit)]:
                    sat_clauses.append(self.clauses.index(clause))
                    break
                elif self.assign_list[abs(lit)] is not None:
                    unsat_count += 1
            if unsat_count == clause.numLits:
                return False

        # remove sat clauses
        if len(sat_clauses) != 0:
            self.numClauses -= len(sat_clauses)
            self.clauses = [clause for i, clause in enumerate(self.clauses) if i not in sat_clauses]

        # update the scores
        for clause in self.clauses:
            for lit in clause.lits:
                self.scores[abs(lit)] += 1

        return True

    def backtrack(self):
        # move up the tree to first lit assigned 1 and assign it 0
        for lit in self.assign_stack[::-1]:
            # undo bcp implications first
            if abs(lit) in self.implied_lits:                 
                self.implied_lits.remove(abs(lit))
                self.assign_list[abs(lit)] = None
                continue
            # then move up the assignment tree
            elif (self.assign_list[abs(lit)] == 0): 
                self.assign_list[abs(lit)] = None
            elif (self.assign_list[abs(lit)] == 1):
                self.assign_list[abs(lit)] = 0
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

        for clause in self.clauses:
            if clause.state == ClauseState.UNRES:
                for lit in clause.lits:
                    self.scores[abs(lit)] += 1
        for lit, _ in self.scores.items():
            self.scores[lit] *= self.decay

        return True

    def bcp(self):
        # find all implications
        sat_count = 0
        implications = set()
        for clause in self.clauses:
            self.update_watched(clause)

            if clause.state == ClauseState.SAT:
                sat_count += 1
                continue

            # add all valid implications
            elif clause.is_unit:
                for lit in clause.lits:
                    if self.assign_list[abs(lit)] is None:
                        if -lit in implications:
                            self.bcp_success = 0
                            return False
                        implications.add(lit)
                        break

        # return if sat
        if sat_count == self.numClauses:
            self.bcp_success = False
            self.sat = 1
            return False

        # return to assign new literal, no more implications
        if len(implications) == 0:
            self.bcp_success = 0
            return True

        # assign the generated implications
        for imply in implications:
            self.assign_list[abs(imply)] = 1 if abs(imply) == imply else 0
            self.assign_stack.append(abs(imply))
            self.implied_lits.append(abs(imply))

        self.bcp_success = 1
        return True

    def forward(self):
        # find next largest scored literal and assign 1
        for lit in sorted(self.scores.items(), key=lambda x: -x[1]):
            lit = int(lit[0])
            if self.assign_list[lit] == None:
                self.assign_list[lit] = 1
                self.assign_stack.append(lit)
                return True
        return False

    def next_literal(self):
        self.bcp_success = 1
        valid = 1
        while self.bcp_success:
            valid = self.bcp()

        if self.sat:
            return False
        elif not valid: # need to backtrack
            if not self.backtrack():
                return False
            for clause in self.clauses: # reset watched literals
                clause.watched = [0, 1]
        elif self.bcp_success == 0: # need to assign new literal
            self.forward()

        return True

    def solve(self):
        if not self.preprocess():
            self.sat = 0
            return

        score_count = 0
        while self.next_literal():
            score_count += 1
            if score_count % 5 == 0:
                self.decay *= self.decay
            pass

        for lit, val in self.assign_list.items():
            if val is None:
                self.assign_list[lit] = 0

        if self.sat:
            print("RESULT: SAT")
            print("ASSIGNMENT: ", end = '')
            for key, value in self.assign_list.items():
                print(f'{key}={value}', end=' ')
            print()
        else:
            print("RESULT: UNSAT")

        return 0
