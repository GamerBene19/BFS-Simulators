import re
import argparse
import warnings


def make_wide(formatter, w=120, h=36):
    # See https://stackoverflow.com/a/57655311
    """Return a wider HelpFormatter, if possible."""
    try:
        # https://stackoverflow.com/a/5464440
        # beware: "Only the name of this class is considered a public API."
        kwargs = {'width': w, 'max_help_position': h}
        formatter(None, **kwargs)
        return lambda prog: formatter(prog, **kwargs)
    except TypeError:
        warnings.warn("argparse help formatter failed, falling back.")
        return formatter


parser = argparse.ArgumentParser(
    description='Simulates a Random Access Machine', formatter_class=make_wide(argparse.ArgumentDefaultsHelpFormatter))
parser.add_argument('--verbose', dest='verbose', action='store_true',
                    help='wether or not to print extra information')
parser.add_argument('--interactive', dest='interactive', action='store_true',
                    help='if set execution halts after every step and waits for user to press enter')
parser.add_argument('--path', dest='path', type=str, default='program.txt',
                    help='path to the file that contains the program')
args = parser.parse_args()


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


def goto(lineIdx: str):
    global count
    global line
    if(lineIdx == "END"):
        done()
    count = int(lineIdx)
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


def ifCondition(comparisonOperator: str, comparisonValue: int, cellIdxOnSuccess: str):
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


# Initialize global values
count = 0
cells = [0]

# Read file
lines = open(args.path, 'r').readlines()

# Remove comments
regex = re.compile("^(//|#).*")
for i, line in enumerate(lines):
    lines[i] = regex.sub("", line)

# Commands that are of the form `COMAND([number])`
normalCommands = {
    "LOAD": load,
    "STORE": store,
    "ADD": add,
    "SUB": sub,
    "MULT": mult,
    "DIV": div,
    "END": done,
    "C-LOAD": cLoad,
    "C-ADD": cAdd,
    "C-SUB": cSub,
    "C-MULT": cMult,
    "C-DIV": cDiv,
    "IND-LOAD": indLoad,
    "IND-STORE": indStore,
    "IND-ADD": indAdd,
    "IND-SUB": indSub,
    "IND-MULT": indMult,
    "IND-DIV": indDiv,
}

line = lines[0]
while(True):
    # Display verbose output
    if(args.verbose):
        print("Counter: {} Cells: {}".format(count, cells))
        print("Next command is: {}".format(line))
    # Enable interactive mode
    if(args.interactive):
        input("Press Enter to continue...")
    # Skip empty lines
    if (len(line.strip()) == 0):
        if (count+1 >= len(lines)):
            done()
        line = lines[count+1]

    # Match different commands
    endMatch = re.findall("^END", line, flags=re.MULTILINE)
    normalMatch = re.findall(
        "^(LOAD|STORE|ADD|SUB|MULT|DIV|END|C-LOAD|C-ADD|C-SUB|C-MULT|C-DIV|IND-LOAD|IND-STORE|IND-ADD|IND-SUB|IND-MULT|IND-DIV)\((\d+)\)", line, flags=re.MULTILINE)
    gotoMatch = re.findall("^(GOTO) (\d+|END)", line, flags=re.MULTILINE)
    ifMatch = re.findall(
        "^(IF) C0 (=|<=|>=|<|>) (\d+) (GOTO) (\d+|END)", line, flags=re.MULTILINE)

    if(len(endMatch) > 0):
        done()
    elif (len(normalMatch) > 0):
        command = normalMatch[0][0]
        commandValue = int(normalMatch[0][1])
        normalCommands[command](commandValue)
        increaseCountAndSetNextLine()
    elif(len(gotoMatch) > 0):
        goto(gotoMatch[0][1])
    elif(len(ifMatch) > 0):
        ifCondition(ifMatch[0][1], int(ifMatch[0][2]), ifMatch[0][4])
    else:
        exit("ERROR: Unknown command in line {}".format(count))
