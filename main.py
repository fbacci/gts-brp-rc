import utils
from transportation import solve_transportation_problem
from Network import Network
from Node import Node
import pandas as pd
from docplex.mp.solution import SolveSolution

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

if __name__ == "__main__":
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
    datasets = [{"instance": "1Bari30.txt", "obj": 14600, "time": "0.06"}]

    for dataset in datasets:
        print(dataset["instance"])

        # read dataset
        n, c, q, Q  = utils.open_dataset("dataset/" + dataset["instance"])

        N = [i for i in range(1, n)]
        V = [0] + N
        A = [(i, j) for i in V for j in V]
        #m = 80

        solution, reduced_costs = solve_transportation_problem(N, n, c, q)
        solution.display()

    #print(df)

    #df.to_csv('df.csv')