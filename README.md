# COMP_560_HW1

In this project, we used three approaches to solve the KenKen puzzle
1. Simple backtracking solution: performance baseline
2. Optimized backtracking solution: most constrained variable
3. Local search solution: greedy descent, simulated annealing, 
and random restarts

Our input is written in a raw test_input.txt file, with the following format:
6
ABBCDD
AEECFD
GGHHFD
GGIJKK
LLIJJM
NNNOOM
A:11+
B:2/
C:20*
D:6*
E:3-
F:3/
G:240*
H:6*
I:6*
J:7+
K:30*
L:6*
M:9+
N:8+
O:2/

## Description
A NxN puzzle is partitioned into different blocks. Each letter
denotes the cells that belong to that block. The constraints for
this puzzle are that: any # can only appear once per row and once
per column. Furthermore, all values of cells within a given block
have to satisfy the mathematical expression of that block.

## Executing Instructions
Interpreter: Python 3.6
Set up the script path and execution environment to run either Solution_1.py,
Solution_2.py, or Solution_3.py.
