# COMP_560_HW1

In this project, we used three approaches to solve the KenKen puzzle
1. Simple backtracking solution: performance baseline
2. Optimized backtracking solution: most constrained variable
3. Local search solution: greedy descent, simulated annealing, 
and random restarts

Our input is written in a raw test_input.txt file, with the following format:<br />
6<br />
ABBCDD<br />
AEECFD<br />
GGHHFD<br />
GGIJKK<br />
LLIJJM<br />
NNNOOM<br />
A:11+ <br />
B:2/ <br />
C:20* <br />
D:6* <br />
E:3- <br />
F:3/ <br />
G:240* <br />
H:6* <br />
I:6* <br />
J:7+ <br />
K:30* <br />
L:6* <br />
M:9+ <br />
N:8+ <br />
O:2/  <br />

## Description
A NxN puzzle is partitioned into different blocks. Each letter
denotes the cells that belong to that block. The constraints for
this puzzle are that: any # can only appear once per row and once
per column. Furthermore, all values of cells within a given block
have to satisfy the mathematical expression of that block.

## Executing Instructions
Interpreter: Python 3.6
Set up the script path and execution environment to run either Solution_1.py,
Solution_2.py, or Solution_3.py.<br />
You need to put the test_input.txt in the same folder.
