import numpy as np
import os
import sys
# read input file
inputs = open(os.getcwd()+"/test_input.txt", "r")
dimension = int(inputs.readline())
characters = np.empty((dimension, dimension), dtype=np.unicode_)
for i in range(dimension):
    curr_row = inputs.readline()
    for j in range(dimension):
        characters[i][j] = curr_row[j]

constraints = inputs.readlines()
constrain = {}
chunk = []
for i in range(len(constraints)):
    curr_row = constraints[i]
    chunk.append(curr_row[0])
    num = ''
    operator = None
    for j in range(2, len(curr_row)):
        if (curr_row[j].isdigit()):
            num = num + curr_row[j]
        elif (curr_row[j] == '*' or '+' or '/' or '-' or ' '):
            operator = curr_row[j]
            break
    value = (num, operator)
    constrain[curr_row[0]] = value

coordinator_chunk = {}
for i in range(dimension):
    for j in range(dimension):
        curr_char = characters[i][j]
        if curr_char in coordinator_chunk:
            coordinators = coordinator_chunk[curr_char]
            coordinators.append((i, j))
            coordinator_chunk[curr_char] = coordinators
        else:
            coordinator_chunk[curr_char] = [(i, j)]

# coordinator_values
coordinator_values = np.zeros((dimension, dimension))
for i in range(dimension):
    for j in range(dimension):
        coordinator_values[i][j] = None

all_values = []
for i in range(dimension):
    all_values.append(i + 1)


# tree implementation

class Node():
    def __init__(self, data=None, next=None, previous=None, coordinator=None):
        self.data = data
        self.next = next
        self.previous = previous
        self.coordinator = coordinator


dummyhead = Node()
curr_node = Node(coordinator=(0, 0))
dummyhead.next = curr_node
curr_node.previous = dummyhead

count = 0

while (True):
    # dummy = 0;
    # for i in range(dimension):
    #     for j in range(dimension):
    #         if not np.isnan(coordinator_values[i][j]):
    #             dummy = dummy + 1
    # if (dummy == dimension * dimension):
    #     break
    row = curr_node.coordinator[0]
    column = curr_node.coordinator[1]
    possible_values = all_values.copy()
    # 减去 row and column
    for i in range(dimension):
        if coordinator_values[row][i] in possible_values:
            possible_values.remove(coordinator_values[row][i])
        if coordinator_values[i][column] in possible_values:
            possible_values.remove((coordinator_values[i][column]))

    # 减去 constrain
    character = characters[row][column]
    cst_cor = coordinator_chunk[character]
    cst_num = int(constrain[character][0])
    cst_op = constrain[character][1]
    cst_cor_values = []
    for i in range(len(cst_cor)):
        if cst_cor[i][0] == row and cst_cor[i][1] == column:
            continue
        else:
            # add related coordinators' values
            if not np.isnan(coordinator_values[cst_cor[i][0]][cst_cor[i][1]]):
                cst_cor_values.append(coordinator_values[cst_cor[i][0]][cst_cor[i][1]])

    remove_list = []

    for i in range(len(possible_values)):
        if cst_op == '+':
            sum = possible_values[i]
            for j in range(len(cst_cor_values)):
                sum += cst_cor_values[j]
            if sum > cst_num or (len(cst_cor) - 1 == len(cst_cor_values) and sum < cst_num):
                remove_list.append(possible_values[i])
        elif cst_op == '-':
            if len(cst_cor_values) == 0:
                continue
            else:
                if abs(cst_cor_values[0] - possible_values[i]) != cst_num:
                    remove_list.append(possible_values[i])
        elif cst_op == '*':
            mul = possible_values[i]
            for j in range(len(cst_cor_values)):
                mul *= cst_cor_values[j]
            if mul > cst_num or (len(cst_cor) - 1 == len(cst_cor_values) and mul < cst_num):
                remove_list.append(possible_values[i])
        elif cst_op == '/':
            if len(cst_cor_values) == 0:
                continue
            else:
                if cst_cor_values[0] / possible_values[i] != cst_num and possible_values[i] / cst_cor_values[0] != cst_num:
                    remove_list.append(possible_values[i])
        else:
            possible_values = [cst_num]
            break
    for i in range(len(remove_list)):
        possible_values.remove(remove_list[i])
    # assign the first value in the possible value list
    curr_node.data = possible_values

    while (len(curr_node.data) == 0):
        curr_node = curr_node.previous
        curr_node.next = None
        try:
            row = curr_node.coordinator[0]
            column = curr_node.coordinator[1]
        except:
            sys.exit('No Solution')
        del curr_node.data[0]
        coordinator_values[row][column] = None

    coordinator_values[row][column] = curr_node.data[0]

    check_nodes = []
    for i in range(dimension):
        for j in range(dimension):
            if np.isnan(coordinator_values[i][j]):
                check_nodes.append((i, j))
    # node that are non
    if len(check_nodes)==0:
        break
    coor_list = []
    min_len = -1

    for i in range(len(check_nodes)):
        possible_values1 = all_values.copy()
        row1 = check_nodes[i][0]
        column1 = check_nodes[i][1]

        # remove row and column values
        for i in range(dimension):
            if coordinator_values[row1][i] in possible_values1:
                possible_values1.remove(coordinator_values[row1][i])
            if coordinator_values[i][column1] in possible_values1:
                possible_values1.remove((coordinator_values[i][column1]))

        # remove constrain values
        character = characters[row1][column1]
        cst_cor = coordinator_chunk[character]  # corresponding tuples
        cst_num = int(constrain[character][0])
        cst_op = constrain[character][1]
        cst_cor_values = []  # doesn't contain itself
        for i in range(len(cst_cor)):
            if cst_cor[i][0] == row1 and cst_cor[i][1] == column1:
                continue
            else:
                # add related coordinators' values
                if not np.isnan(coordinator_values[cst_cor[i][0]][cst_cor[i][1]]):
                    cst_cor_values.append(coordinator_values[cst_cor[i][0]][cst_cor[i][1]])

        remove_list = []

        for i in range(len(possible_values1)):
            if cst_op == '+':
                sum = possible_values1[i]
                for j in range(len(cst_cor_values)):
                    sum += cst_cor_values[j]
                if sum > cst_num or (len(cst_cor) - 1 == len(cst_cor_values) and sum < cst_num):
                    remove_list.append(possible_values1[i])
            elif cst_op == '-':
                if len(cst_cor_values) == 0:
                    continue
                else:
                    if abs(cst_cor_values[0] - possible_values1[i]) != cst_num:
                        remove_list.append(possible_values1[i])
            elif cst_op == '*':
                mul = possible_values1[i]
                for j in range(len(cst_cor_values)):
                    mul *= cst_cor_values[j]
                if mul > cst_num or (len(cst_cor) - 1 == len(cst_cor_values) and mul < cst_num):
                    remove_list.append(possible_values1[i])
            elif cst_op == '/':
                if len(cst_cor_values) == 0:
                    continue
                else:
                    if cst_cor_values[0] / possible_values1[i] != cst_num and possible_values1[i] / cst_cor_values[
                        0] != cst_num:
                        remove_list.append(possible_values1[i])
            else:
                possible_values1 = [cst_num]
                break

        for i in range(len(remove_list)):
            possible_values1.remove(remove_list[i])

        c = len(possible_values1)

        if min_len == -1:
            min_len = c
            coor_list.append((row1, column1))
        elif min_len > c:
            min_len = c
            coor_list.clear()
            coor_list.append((row1, column1))
        elif min_len == c:
            coor_list.append((row1, column1))

        # min keep track of the smallest one possible values and coordinator
        next_row = coor_list[0][0]
        next_column = coor_list[0][1]

    next_node = Node(coordinator=(next_row, next_column))
    curr_node.next = next_node
    next_node.previous = curr_node
    curr_node = next_node
    count = count + min_len

print(coordinator_values)
print(count)
