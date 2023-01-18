#!/usr/bin/env python3.10
import sys


m_filename = sys.argv[1]

v = 0
V = []
I = {}
F = []
with open(m_filename) as file:
    for line in file:
        match line.split():
            case ["Vertex",i,x,y,z]:
                V.append((x,y,z))
                I[(int(i))] = len(V)
            case ["Face",j,a,b,c]:
                F.append([I[int(x)] for x in (a,b,c)])

with open(sys.argv[2], 'w') as f:
    [print(f'v {x[0]} {x[1]} {x[2]}',file=f) for x in V]
    [print(f'f {x[0]} {x[1]} {x[2]}',file=f) for x in F]
