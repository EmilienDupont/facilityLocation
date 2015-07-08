#!/usr/bin/env python

from gurobipy import *
import math

points = [[100,200], [150,250], [650, 200], [50, 300]];

facilities = []; charge = [];

for i in range(10):
    for j in range(10):
        facilities.append([i*70, j*50])
        charge.append(1)

# Might need to move this stuff into javascript
def distance(a,b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx*dx + dy*dy)

numFacilities = len(facilities)

numClients = len(points)

m = Model()

# Add variables
x = {}
y = {}
d = {} # Distance matrix

for j in range(numFacilities):
    x[j] = m.addVar(vtype=GRB.BINARY, name="x%d" % j)

# Distance is symmetric, so should we only do half the variables?
for i in range(numClients):
    for j in range(numFacilities):
        y[(i,j)] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="t%d,%d" % (i,j))
        d[(i,j)] = distance(points[i], facilities[j])

m.update()

# Add constraints
for i in range(numClients):
    for j in range(numFacilities):
        m.addConstr(y[(i,j)] <= x[j])

for i in range(numClients):
    m.addConstr(quicksum(y[(i,j)] for j in range(numFacilities)) == 1)

m.setObjective( quicksum( charge[j]*x[j] + quicksum(d[(i,j)]*y[(i,j)] for i in range(numClients))
                         for j in range(numFacilities) ), GRB.MINIMIZE)

m.optimize()

for j in range(numFacilities):
    print x[j]