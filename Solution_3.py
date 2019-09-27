import sys
import random
import math

# Properties: row, col, val


class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.val = 0;
        # cell_name.val = x --> to set property
        # del cell_name.val --> to delete property

# Properties: constraint # - n, constraint operation - op, cells that belong to block - cells


# TODO: if block op is just a #?
class Block:
    def __init__(self, id, n: int, op):
        self.id = id
        self.n = n
        self.op = op
        self.cells = set()
        # set.add() --> 1 element
        # set.update() --> multiple elements
        # set.remove() -->  1 element, raises error if item doesn't exist
        # set.discard() --> 1 element, leaves set as is if item doesn't exist
        # set.clear() --> multiple elements

# Helper function


def print_cells():
    for k, v in cells.items():
        print("---------- CELL " + k + " ----------")
        print("(" + str(v.row) + "," + str(v.col) + ") -> val: " + str(v.val))

# Helper function


def print_blocks():
    for k, v in blocks.items():
        print("---------- BLOCK " + k + " ----------")
        print("n: " + v.n + " op: " + v.op)
        cells_str = ""
        for c in v.cells:
            cells_str += "(" + str(c.row) + "," + str(c.col) + ") "
        print(cells_str)

# Helper function


def print_state(cells):
    counter = 0
    line = "| "

    print("----------- STATE -----------")
    for c in cells.values():
        line += str(c.val) + " | "
        counter += 1
        if counter == N:
            print(line)
            counter = 0
            line = "| "
    print("-----------------------------")


# TODO: delete?
def set_domain():
    for i in range(N):
        dom.add(i + 1)


def initialize_state(N, cells):
    for r in range(N):
        for c in range(N):
            cells[str(r) + str(c)].val = random.randint(1, N)


def check_block(block):
    # Find cells in same block
    # print("---------- BLOCK " + block.id + " ----------")
    # print("n: " + block.n + " op: " + block.op)

    # Block val stores the quantitative result of each block
    # Initialize block val to 0 for addition/subtraction and 1 for multiplication/division.
    if block.op == '+':
        block_val = 0
    elif block.op == '-':
        block_val = 0.5  # Reassign later: A - B won't yield non-whole #
    elif block.op == '*':
        block_val = 1
    elif block.op == '/':
        block_val = -1  # Reassign later: A / B won't yield negative #

    for c in block.cells:
        if block.op == '+':
            block_val += c.val
        elif block.op == '-':
            if block_val == 0.5:
                block_val = c.val
            else:
                block_val -= c.val
        elif block.op == '*':
            block_val *= c.val
        elif block.op == '/':
            if block_val == -1:
                block_val = c.val
            else:
                block_val /= c.val
        # print("(" + str(c.row) + ", " + str(c.col) + ") = " + str(c.val) + " --> block curr = " + str(block_val))

    if block_val <= 0:  # Subtraction: used min - max --> take abs val
        block_val = abs(block_val)
    elif block_val < 1:  # Division: used min / max --> take inverse
        block_val = 1 / block_val
    # print("block final: " + str(block_val))
    # print("-----------------------------")
    return block_val

# Scan board to tally num violations cell value creates


def num_violations(cell):
    count = 0

    cell_col = cell.col
    cell_row = cell.row

    # Check for duplicates in the same col
    for r in range(N):
        # Refrain from counting self as a violation
        if r == cell_row:
            # print("col of: " + str(cell.val))
            continue
        curr_cell = cells[str(r) + str(cell_col)]
        if curr_cell.val == cell.val:
            # print("col collision: " + str(curr_cell.val))
            count += 1

    # Check for duplicates in the same row
    for c in range(N):
        # Refrain from counting self as a violation
        if c == cell_col:
            # print("row of: " + str(cell.val))
            continue
        curr_cell = cells[str(cell_row) + str(c)]
        if curr_cell.val == cell.val:
            # print("row collision: " + str(curr_cell.val))
            count += 1

    # Check for duplicates within same block
    for block_id, block in blocks.items():
        # Find which block the cell belongs in
        if cell in block.cells:
            block_val = check_block(block)
            # Comparison needs to be type consistent
            if block_val != int(block.n):
                # print("block collision...")
                # print("block target: " + str(block.n))
                count += 1
    # print("(" + str(cell.row) + "," + str(cell.col) + ") -> violations: " + str(count))
    # print("-----------------------------")
    return count


# ---------- MAIN LOGIC STARTS HERE ----------
f = open("test_input.txt", "r")
N = int(f.readline())
iterations = 0

# Maps block id to block object
blocks = dict()
# Maps coord to cell object
cells = dict()

# TODO: delete?
# dom = set()
# set_domain()
# print("Domain: " + str(dom))

for i in range(N):
    line = f.readline()
    for j in range(len(line)):
        bid = line[j]
        if bid == '\n':
            break

        curr_cell = Cell(i, j)
        cells[str(i) + str(j)] = curr_cell
        if bid not in blocks:
            curr_block = Block(bid, 0, '')
            # Add cell to block
            curr_block.cells.add(curr_cell)
            # Add block to blocks dict
            blocks[bid] = curr_block
        else:
            blocks[bid].cells.add(curr_cell)

# Make sure to add new line at the end of test_input.txt!
for i in range(len(blocks.keys())):
    # Equation
    eq = f.readline()
    # Parsing equation
    bid = eq[0]
    # Access last symbol of eq, len - 2 bc of \n.
    n = eq[2:len(eq) - 2]
    op = eq[len(eq) - 2]
    # Assign to blocks
    blocks[bid].n = n
    blocks[bid].op = op

# Test output
print_blocks()

# Goal: 0 constraint violations
reached_global_min = False

# Allowing N random restarts
for restarts in range(1, N):
    if not reached_global_min:

        # Initial state: assign a random value within domain to every cell.
        initialize_state(N, cells)
        iterations += 1
        # Test output
        print_cells()
        # print_state(cells)

        min_violations = 0
        total_violations = 0

        # Calculate initial violations
        for r in range(N):
            for c in range(N):
                # Set min violations to num violations of initial state
                cell = cells[str(r) + str(c)]
                min_violations += num_violations(cell)

        print("# of initial violations: " + str(min_violations))

        # Initial state is correct answer
        if min_violations == 0:
            reached_global_min = True
            break

        # Simulated annealing
        for t in range(sys.maxsize**10, 1, -1):
            total_violations = 0

            # Pick a random cell
            r = random.randint(0, N - 1)
            c = random.randint(0, N - 1)
            cell = cells[str(r) + str(c)]
            changed_row = cell.row
            changed_col = cell.col

            # Assign a random value within domain to cell
            curr_val = cell.val
            cell.val = random.randint(1, N)
            iterations += 1

            # Calculate violations of neighbor state
            for i in range(N):
                for j in range(N):
                    cell = cells[str(i) + str(j)]
                    total_violations += num_violations(cell)

            # Terminate once all constraints are satisfied
            if total_violations == 0:
                print("Final violations: " + str(min_violations))
                min_violations = total_violations
                print("---------- SOLUTION ----------")
                print("Final violations: " + str(min_violations))
                print("Total iterations: " + str(iterations))
                print_state(cells)
                reached_global_min = True
                break
            else:
                # "Energy" of state
                delta_e = total_violations - min_violations
                # Min violations fluctuates since we are not always making the local best choice
                # print("Curr violations: " + str(min_violations))
                # If total_violations < min_violations, always proceed to neighbor state
                if delta_e < 0:
                    min_violations = total_violations
                    # print("Move to better state: " + str(min_violations))
                else:  # Only proceed to next state with P(e^(delta_e/t))
                    prob_move = math.e ** (delta_e / t)
                    # print("P(move to worse state): " + str(prob_move))
                    # Do not proceed to neighbor state by reversing cell value change
                    if not prob_move > random.randint(0, 1):
                        # print("Stay as is: " + str(min_violations))
                        cell.val = curr_val
                    else:
                        min_violations = total_violations
                        # print("Move to worse state: " + str(min_violations))

            # Trigger random restart
            if random.randint(0, N ** 10) <= N ** (N - 1):
                print("---------- Restart # " + str(restarts) + "----------")
                print("Last recorded violations: " + str(min_violations))
                break

if not reached_global_min:
    print("---------- NO SOLUTION FOUND ----------")
    print("Final violations: " + str(min_violations))
    print("Total iterations: " + str(iterations))
    print_state(cells)

# TODO: have a matrix mapping num violations for each cell?
