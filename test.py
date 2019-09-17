import numpy as np

#read input file
inputs=open("/Users/IssacQI/Desktop/test_input.txt","r")

dimension=int(inputs.readline())
print(dimension)
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
        elif(curr_row[j]=='*' or '+' or '/' or '-'):
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


# tree implementation








