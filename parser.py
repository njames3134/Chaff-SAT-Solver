clauseArr = []
literalArr = []

numLits = 0
numClauses = 0

def parseInput(filename):
    file = open(filename, 'r')
        for (line in file.readlines()):
            if (line.startswith('p')):
                
            elif(line.startswith('c')):
                pass
            else:
                clause = Clause()
                