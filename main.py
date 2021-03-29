import utils
from Network import Network
from Node import Node
import pandas as pd
from docplex.mp.solution import SolveSolution
from docplex.mp.model import Model
from copy import deepcopy
from itertools import repeat

"""
n: station number
N: stations without deposit
V: stations with deposit
A: arcs
m: vehicle number
Q: vehicle capacity
q: demand at stations
c: cost matrix
"""

df = pd.DataFrame(columns=['Instance', 'Our obj', 'Paper Obj', 'Our Time', 'Paper Time', 'GAP'])

datasets = [
            {"instance": "1Bari30.txt", "obj": 14600, "time": "0.06"},
            {"instance": "2Bari20.txt", "obj": 15700, "time": "0.06"},
            {"instance": "3Bari10.txt", "obj": 20600, "time": "0.16"},
            {"instance": "4ReggioEmilia30.txt", "obj": 16900, "time": "0.03"},
            {"instance": "5ReggioEmilia20.txt", "obj": 23200, "time": "0.09"},
            {"instance": "6ReggioEmilia10.txt", "obj": 32500, "time": "5.59"},
            {"instance": "7Bergamo30.txt", "obj": 12600, "time": "0.05"},
            {"instance": "8Bergamo20.txt", "obj": 12700, "time": "0.06"},
            {"instance": "9Bergamo12.txt", "obj": 13500, "time": "0.27"},
            {"instance": "10Parma30.txt", "obj": 29000, "time": "0.05"},
            {"instance": "11Parma20.txt", "obj": 29000, "time": "0.05"},
            {"instance": "12Parma10.txt", "obj": 32500, "time": "0.22"},
            {"instance": "13Treviso30.txt", "obj": 29259, "time": "0.12"},
            {"instance": "14Treviso20.txt", "obj": 29259, "time": "0.12"},
            {"instance": "15Treviso10.txt", "obj": 31443, "time": "0.27"},
            {"instance": "16LaSpezia30.txt", "obj": 20746, "time": "0.09"},
            {"instance": "17LaSpezia20.txt", "obj": 20746, "time": "0.09"},
            {"instance": "18LaSpezia10.txt", "obj": 22811, "time": "0.16"},
            {"instance": "19BuenosAires30.txt", "obj": 76999 , "time": "1.36"},
            {"instance": "20BuenosAires20.txt", "obj": 91619, "time": "23.26"},
            {"instance": "21Ottawa30.txt", "obj": 16202, "time": "0.06"},
            {"instance": "22Ottawa20.txt", "obj": 16202, "time": "0.06"},
            {"instance": "23Ottawa10.txt", "obj": 17576, "time": "0.3"},
            {"instance": "24SanAntonio30.txt", "obj": 22982 , "time": "0.19"},
            {"instance": "25SanAntonio20.txt", "obj": 24007, "time": "3.63"},
            {"instance": "27Brescia30.txt", "obj": 30300, "time": "0.7"},
            {"instance": "28Brescia20.txt", "obj": 31100, "time": "6.07"},
            {"instance": "29Brescia11.txt", "obj": 35200, "time": "24.46"},
            {"instance": "30Roma30.txt", "obj": 61900, "time": "4.27"},
            {"instance": "31Roma20.txt", "obj": 66600, "time": "22.04"},
            {"instance": "32Roma18.txt", "obj": 68300, "time": "16.15"},
            {"instance": "33Madison30.txt", "obj": 29246, "time": "0.09"},
            {"instance": "34Madison20.txt", "obj": 29839, "time": "0.31"},
            {"instance": "35Madison10.txt", "obj": 33848, "time": "6.02"},
            {"instance": "36Guadalajara30.txt", "obj": 57476, "time": "1.16"},
            {"instance": "37Guadalajara20.txt", "obj": 59493, "time": "2.29"}
           ]
datasets = [ {"instance": "1Bari30.txt", "obj": 14600, "time": "0.06"}]

for dataset in datasets:
    print(dataset["instance"])

    # read dataset
    n, c, q, Q  = utils.open_dataset("dataset/" + dataset["instance"])

    N = [i for i in range(1, n)]
    V = [0] + N
    A = [(i, j) for i in V for j in V]
    #m = 80

    # Transshipment Problem
    model = Model(name='transshipment')

    c_copy = deepcopy(c)

    #split nodes in supply (source) and deficit(target)
    target = []
    source = []
    total_demand = 0
    total_supply = 0

    for node in N:
        if q[node] < 0:
            total_demand += q[node]
            target.append((node, q[node]))
        else:
            total_supply += q[node]
            source.append((node, q[node]))

    print(total_demand, total_supply)

    # generate artificial nodes
    if abs(total_demand) > total_supply:
        source.append((n, abs(total_demand) - total_supply))
        for (t, q) in target:
            c_copy[(n, t)] = 0
    else:
        target.append((n, -(total_supply - abs(total_demand))))
        for(s, q) in source:
            c_copy[(s, n)] = 0

    print(source, target)

    # initialize decision variable
    x = {(s,t): model.continuous_var(name='x_{0}_{1}'.format(s,t)) for (s, _) in source for (t, _) in target}

    # minimize flow cost
    model.minimize(model.sum(x[s,t]*c_copy.get((s,t), 0) for (s, _) in source for (t, _) in target))

    # set constraints
    # for each source node, total outgoing flow must be smaller than available quantity
    for (s, q) in source:
        model.add_constraint(model.sum(x[s,t] for (t, _) in target) <= q)
        
    # for each target node, total ingoing flow must be greater than demand
    for (t, q) in target:
        model.add_constraint(model.sum(x[s,t] for (s, _) in source) >= abs(q))

    #model.print_information()

    solution = model.solve()
    solution.display()
    reduced_costs = model.reduced_costs(x[s,t] for (s, _) in source for (t, _) in target)

    i = 0
    reduced_costs_index = []
    for (s, _) in source:
        for (t, _) in target:
            reduced_costs_index.append(((s,t), reduced_costs[i]))
            i += 1

    print(reduced_costs_index)

    #if solution is None:
    #    new_value = {'Instance': dataset["instance"],  'Our obj': "None", 'Paper Obj': dataset["obj"], 'Our Time': "none", 'Paper Time': dataset["time"], 'GAP': "None"}
    #else:
    #    solve_details = solution.solve_details
    #    new_value = {'Instance': dataset["instance"],  'Our obj': solution.get_objective_value(), 'Paper Obj': dataset["obj"], 'Our Time': solve_details.time, 'Paper Time': dataset["time"], 'GAP': "{:.2f}".format(100*solution.get_objective_value()/dataset["obj"]-100)}

    #print(new_value)

    #df = df.append(new_value, ignore_index=True)

#print(df)

#df.to_csv('df.csv')