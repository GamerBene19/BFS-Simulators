import re


def done():
    exit("Reached end of execution!\nFinal state: Counter: {}\tCells: {}".format(
        count, cells))


def increaseCountAndSetNextLine():
    global count
    global line
    count += 1
    if (count >= len(lines)):
        done()
    line = lines[count]


def goto(lineIdx: int):
    global count
    global line
    count = lineIdx
    if (count >= len(lines)):
        done()
    line = lines[count]


def load(cellIdx: int):
    cells[0] = cells[cellIdx]


def store(cellIdx: int):
    cells.extend([0] * (cellIdx-(len(cells)-1)))
    cells[cellIdx] = cells[0]


def add(cellIdx: int):
    cells[0] += cells[cellIdx]


def sub(cellIdx: int):
    cells[0] -= cells[cellIdx]
    if (cells[0] < 0):
        cells[0] = 0


def mult(cellIdx: int):
    cells[0] *= cells[cellIdx]


def div(cellIdx: int):
    cells[0] //= cells[cellIdx]


def cLoad(value: int):
    cells[0] = value


def cAdd(value: int):
    cells[0] += value


def cSub(value: int):
    cells[0] -= value
    if (cells[0] < 0):
        cells[0] = 0


def cMult(value: int):
    cells[0] *= value


def cDiv(value: int):
    cells[0] //= value


def indLoad(cellIdx: int):
    cells[0] = cells[cells[cellIdx]]


def indStore(cellIdx: int):
    store(cells[cellIdx])


def indAdd(cellIdx: int):
    cells[0] += cells[cells[cellIdx]]


def indSub(cellIdx: int):
    cells[0] -= cells[cells[cellIdx]]
    if (cells[0] < 0):
        cells[0] = 0


def indMult(cellIdx: int):
    cells[0] *= cells[cells[cellIdx]]


def indDiv(cellIdx: int):
    cells[0] //= cells[cells[cellIdx]]


def ifCondition(comparisonOperator: str, comparisonValue: int, cellIdxOnSuccess: int):
    conditionIsTrue = False
    if(comparisonOperator == "=" and cells[0] == comparisonValue):
        conditionIsTrue = True
    elif(comparisonOperator == ">" and cells[0] > comparisonValue):
        conditionIsTrue = True
    elif(comparisonOperator == ">=" and cells[0] >= comparisonValue):
        conditionIsTrue = True
    elif(comparisonOperator == "<" and cells[0] < comparisonValue):
        conditionIsTrue = True
    elif(comparisonOperator == "<=" and cells[0] <= comparisonValue):
        conditionIsTrue = True

    if(conditionIsTrue):
        goto(cellIdxOnSuccess)
    else:
        increaseCountAndSetNextLine()


count = 0
cells = [0]
lines = open('program.txt', 'r').readlines()
line = lines[0]
while(True):
    print("Counter: {} Cells: {}".format(count, cells))
    normalMatch = re.findall(
        "^(LOAD|STORE|ADD|SUB|MULT|DIV|GOTO|END|C-LOAD|C-ADD|C-SUB|C-MULT|C-DIV|IND-LOAD|IND-STORE|IND-ADD|IND-SUB|IND-MULT|IND-DIV)\((\d+)\)", line, flags=re.MULTILINE)
    gotoMatch = re.findall("^(GOTO) (\d+)", line, flags=re.MULTILINE)
    ifMatch = re.findall(
        "^(IF) C0 (=|<=|>=|<|>) (\d+) (GOTO) (\d+)", line, flags=re.MULTILINE)
    if (len(normalMatch) > 0):
        operation = normalMatch[0][0]
        opValue = int(normalMatch[0][1])
        if (operation == "LOAD"):
            load(opValue)
        if (operation == "STORE"):
            store(opValue)
        if (operation == "ADD"):
            add(opValue)
        if (operation == "SUB"):
            sub(opValue)
        if (operation == "MULT"):
            mult(opValue)
        if (operation == "DIV"):
            div(opValue)
        if (operation == "C-LOAD"):
            cLoad(opValue)
        if (operation == "C-ADD"):
            cAdd(opValue)
        if (operation == "C-SUB"):
            cSub(opValue)
        if (operation == "C-MULT"):
            cMult(opValue)
        if (operation == "C-DIV"):
            cDiv(opValue)
        if (operation == "IND-LOAD"):
            indLoad(opValue)
        if (operation == "IND-STORE"):
            indStore(opValue)
        if (operation == "IND-ADD"):
            indAdd(opValue)
        if (operation == "IND-SUB"):
            indSub(opValue)
        if (operation == "IND-MULT"):
            indMult(opValue)
        if (operation == "IND-DIV"):
            indDiv(opValue)
        increaseCountAndSetNextLine()

    elif(len(gotoMatch) > 0):
        goto(int(gotoMatch[0][1]))
    elif(len(ifMatch) > 0):
        ifCondition(ifMatch[0][1], int(ifMatch[0][2]), int(ifMatch[0][4]))
    else:
        exit("ERROR: Unknown command in line {}".format(count))
