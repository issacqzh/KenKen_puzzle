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

## How to run the code
Interpreter: Python 3.6
Set up the script path and execution environment to run either Solution_1.py,
Solution_2.py, or Solution_3.py.

## Solution 3 Description
By definition, a local search strategy retains no memory of previous states. Given a neighboring state that differs in the value of 1 cell, this solution utilizes a greedy approach to determine whether or not to transition to the next state or stay in the current one.

We randomly assign values within the domain to all cells, which we consider as the initial state. Then we randomly pick a cell, change the value and evaluate how it compares to the initial state.

The heuristic, or fitness function, used to guide the search is the number of violations given a fully populated KenKen puzzle. We use the simulated annealing optimization method to make decisions. If the next state contains less violations than our current state then we definitely consider the next state. If not, we take it with probability P(eenergy/temp)where temperature decreases over time and energy is just a measure of the difference between the next and current state.

Our ultimate goal is to reach the global minimum in which 0 constraints are violated. By the same logic, a local minimum is defined by the case where most constraints are fulfilled but there are still some violated. (Furthermore, there are no more downhill moves possible given this configuration.)

Since this solution could possibly get stuck in a local minimum where no further moves can be made, we allowed for up to N (size of board) restarts. Restarts are triggered randomly by a conditional that varies based on the size of the board.

## Solution 3 Pseudocode
For restarts 1 → N:
	If violations != 0:
		Initialize state
		Count initial violations
		For t infinity → 1:
			Pick a cell and change its value
			Count updated violations
				If updated violations == 0 → done
				Else
            If updated violations < initial violations
						  Transition to neighboring state
            Else 
              Only transition to neighboring state with P(e^delta_energy/temp) 
       Trigger random restarts
