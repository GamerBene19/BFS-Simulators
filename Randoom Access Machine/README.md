# What is this?

This is a simulator for a Random Access Machine (as defined in our course)

# Usage

## Program input

The program excepts a `program.txt` file located in the same directory as itself. That program has to consist of [supported commands](#supported-commands) each in its own line.  
If a unknown string is encountered the program exits and prints the line-number (0-indexed) that caused it to exit.  
Empty lines and lines starting with `//` or `#` are skipped (but you still have to set your `GOTO`s correctly (as if the lines were filled with normal code))

## Supported Commands

As introduced in our course the RAM supports the following commands:

> Despite the look of the command, the `IF` operation only ever compares to c(0). E.g. `IF C1 = 0 GOTO 0` is not considered valid

| Command            | Action               | Counter                                    | Description                                                                                                  |
| ------------------ | -------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `LOAD(i)`          | `c(0)=c(i)`          | `b=b+1`                                    | Loads value of cell i into accumulator (c0)                                                                  |
| `STORE(i)`         | `c(i)=c(0)`          | `b=b+1`                                    | Stores value of accumulator into i                                                                           |
| `ADD(i)`           | `c(0)=c(0)+c(i)`     | `b=b+1`                                    | Adds value in cell i to accumulator                                                                          |
| `SUB(i)`           | `c(0)=c(0)-c(i)`     | `b=b+1`                                    | Subtracts value in cell i from accumulator (min value is 0)                                                  |
| `MULT(i)`          | `c(0)=c(0)*c(i)`     | `b=b+1`                                    | Multiplies value in cell i with accumulator                                                                  |
| `DIV(i)`           | `c(0)=c(0)/c(i)`     | `b=b+1`                                    | Divides accumulator by value in cell i (integer division; decimal places are discarded)                      |
| `GOTO(j)`          |                      | `b=j`                                      | Sets counter to j                                                                                            |
| `IF C0 ? l GOTO j` |                      | `b=j` if contion is true `b=b+1` otherwise | Sets counter to j if c(0) meets condition (where `?` is from `{=, >=, >, <=, <}` and `l` is a natural number |
| `END`              |                      | no change                                  | Ends program.                                                                                                |
|                    |                      |                                            |                                                                                                              |
| `C-LOAD(l)`        | `c(0)=l`             | `b=b+1`                                    | Same as `LOAD` but uses constant `l`                                                                         |
| `C-ADD(l)`         | `c(0)=c(0)+l`        | `b=b+1`                                    | Same as `ADD` but uses constant `l`                                                                          |
| `C-SUB(l)`         | `c(0)=c(0)-l`        | `b=b+1`                                    | Same as `SUB` but uses constant `l`                                                                          |
| `C-MULT(l)`        | `c(0)=c(0)*l`        | `b=b+1`                                    | Same as `MULT` but uses constant `l`                                                                         |
| `C-DIV(l)`         | `c(0)=c(0)/l`        | `b=b+1`                                    | Same as `DIV` but uses constant `l`                                                                          |
|                    |                      |                                            |                                                                                                              |
| `IND-LOAD(i)`      | `c(0)=c(c(i))`       | `b=b+1`                                    | Same as `LOAD` but uses value stored in `i` as index                                                         |
| `IND-ADD(i)`       | `c(0)=c(0)+c(c(i))l` | `b=b+1`                                    | Same as `ADD` but uses value stored in `i` as index                                                          |
| `IND-SUB(i)`       | `c(0)=c(0)-c(c(i))`  | `b=b+1`                                    | Same as `SUB` but uses value stored in `i` as index                                                          |
| `IND-MULT(i)`      | `c(0)=c(0)*c(c(i))`  | `b=b+1`                                    | Same as `MULT` but uses value stored in `i` as index                                                         |
| `IND-DIV(i)`       | `c(0)=c(0)/c(c(i))`  | `b=b+1`                                    | Same as `DIV` but uses value stored in `i` as index                                                          |

## (Setting) initial values of cells

Cells are created as needed (= when storing to a index that does not exist yet) and initialized with zero.  
Currently there is no support for setting initial values of cells (at beginning of program) so you have to work around it.
Example: Storing value 420 into cell 69

```
C-LOAD(420)
STORE(69)
```

## Example

Stores value 10 into cell 1 and value 2 into cell 2 first and then multiplies value of cell 1 with value of cell 2 and stores output in cell 3. This program can also be found in example.txt. Rename it to program.txt to try it out

```
C-LOAD(10)
STORE(1)
C-LOAD(2)
STORE(2)
LOAD(1)
MUL(2)
STORE(3)
```

## Execution

Assuming you navigated to the correct directory and have created your `program.txt` the RAM-Simulation can be started with:  
`python3.8 RAM.py` (other python3 versions should work too)
