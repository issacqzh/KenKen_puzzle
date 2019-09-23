import numpy as np


#read input file
inputs=open("/Users/IssacQI/Desktop/test_input.txt","r")

dimension=int(inputs.readline())
characters=np.empty((dimension,dimension),dtype=np.unicode_)
for i in range(dimension):
    curr_row=inputs.readline()
    for j in range(dimension):
        characters[i][j]=curr_row[j]

constraints=inputs.readlines()
constrain={}
chunk=[]
for i in range(len(constraints)):
    curr_row=constraints[i]
    chunk.append(curr_row[0])
    num=''
    operator=None
    for j in range(2,len(curr_row)):
        if(curr_row[j].isdigit()):
            num=num+curr_row[j]
        elif(curr_row[j]=='*' or '+' or '/' or '-' or ' '):
            operator=curr_row[j]
            break
    value=(num,operator)
    constrain[curr_row[0]]=value


coordinator_chunk={}
for i in range(dimension):
    for j in range(dimension):
        curr_char=characters[i][j]
        if curr_char in coordinator_chunk:
            coordinators=coordinator_chunk[curr_char]
            coordinators.append((i,j))
            coordinator_chunk[curr_char]=coordinators
        else:
            coordinator_chunk[curr_char]=[(i,j)]


# coordinator_values
coordinator_values=np.zeros((dimension,dimension))
for i in range(dimension):
    for j in range(dimension):
        coordinator_values[i][j]=None

all_values=[]
for i in range(dimension):
    all_values.append(i+1)

# tree implementation

class  Node():
    def __init__(self,data=None,next=None,previous=None,coordinator=None):
        self.data=data
        self.next=next
        self.previous=previous
        self.coordinator=coordinator

dummyhead=Node()
curr_node=Node(coordinator=(0,0))
dummyhead.next=curr_node
curr_node.previous=dummyhead

count=0
while(True):
    row=curr_node.coordinator[0]
    column=curr_node.coordinator[1]
    possible_values=all_values.copy()
    # 减去 row and column
    for i in range(dimension):
        if coordinator_values[row][i] in possible_values:
            possible_values.remove(coordinator_values[row][i])
        if coordinator_values[i][column] in possible_values:
            possible_values.remove((coordinator_values[i][column]))

    # 减去 constrain
    character=characters[row][column]
    cst_cor=coordinator_chunk[character]
    cst_num=int(constrain[character][0])
    cst_op=constrain[character][1]
    cst_cor_values=[]
    for i in range(len(cst_cor)):
        if cst_cor[i][0]==row and cst_cor[i][1]==column:
            continue
        else:
            # add related coordinators' values
            if not np.isnan(coordinator_values[cst_cor[i][0]][cst_cor[i][1]]):
                cst_cor_values.append(coordinator_values[cst_cor[i][0]][cst_cor[i][1]])

    remove_list=[]

    for i in range(len(possible_values)):
        if cst_op=='+':
            sum=possible_values[i]
            for j in range(len(cst_cor_values)):
                sum += cst_cor_values[j]
            if sum > cst_num or (len(cst_cor)-1==len(cst_cor_values) and sum < cst_num):
                remove_list.append(possible_values[i])
        elif cst_op=='-':
            if len(cst_cor_values)==0:
                continue
            else:
                if abs(cst_cor_values[0]-possible_values[i])!=cst_num:
                    remove_list.append(possible_values[i])
        elif cst_op=='*':
            mul=possible_values[i]
            for j in range(len(cst_cor_values)):
                mul *= cst_cor_values[j]
            if mul>cst_num or (len(cst_cor)-1==len(cst_cor_values) and mul<cst_num):
                remove_list.append(possible_values[i])
        elif cst_op=='/':
            if len(cst_cor_values)==0:
                continue
            else:
                if cst_cor_values[0]/possible_values[i] != cst_num and possible_values[i]/cst_cor_values[0] != cst_num:
                    remove_list.append(possible_values[i])
        else:
            possible_values=[cst_num]
            break
    for i in range(len(remove_list)):
        possible_values.remove(remove_list[i])
    # assign the first value in the possible value list
    curr_node.data=possible_values
    count+=len(possible_values)

    while(len(curr_node.data)==0):
        curr_node=curr_node.previous
        curr_node.next=None
        row= curr_node.coordinator[0]
        column=curr_node.coordinator[1]
        del curr_node.data[0]
        coordinator_values[row][column]=None


    coordinator_values[row][column]=curr_node.data[0]

    if row+1>=dimension and column+1>=dimension:
        break
    elif row+1>=dimension:
        next_row=0
        next_column=column+1
    else:
        next_row=row+1
        next_column=column

    next_node = Node(coordinator=(next_row, next_column))
    curr_node.next = next_node
    next_node.previous = curr_node
    curr_node = next_node

print(coordinator_values)
print(count)


