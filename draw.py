import numpy as np
import os
# stringRepr=[
# r"|           _,--=--._           |",
# r"|         ,'    _    `.         |",
# r"|        -    _(_)_o   -        |",
# r"|   ____'    /_  _/]    `____   |",
# r"|-=::(+):::::::::::::::::(+)::=-|", 
# r"|         .           ,         |", 
# r"|___________`  -=-  '___________|",

# ]
# arr=np.array(stringRepr)
# print(len(stringRepr))
# print(len(stringRepr[0]))
# st=""
# for i in range(len(stringRepr)):
#     for j in range(len(stringRepr[0])):
#         st+=arr[i][j]
#     st+='\n'
# os.write(1,str.encode(st))
# import numpy as np

stringRepr=[
                r"|           _,--=--._           |",
                r"|         ,'    _    `.         |",
                r"|        -    _(_)_o   -        |",
                r"|   ____'    /_  _/]    `____   |",
                r"|-=::(+):::::::::::::::::(+)::=-|", 
                r"|         .           ,         |", 
                r"|___________`  -=-  '___________|",

            ]

arr=np.full([7,33],("^"))
for i in range(7):
    for j in range(33):
        arr[i][j]=stringRepr[i][j]
st=""
for i in range(7):
    for j in range(33):
        st+=arr[i][j]
    st+='\n'
os.write(1,str.encode(st))
