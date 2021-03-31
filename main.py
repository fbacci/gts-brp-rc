import utils
import time
from TabuSearch import TabuSearch
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

    results_file = open("dataset/results.txt", "r").read().split('\n')
    results = utils.open_results(results_file)

    for result in results:
        print(result["instance"])
        # read dataset
        n, c, q, Q  = utils.open_dataset("dataset/" + result["instance"])

        def cost_function(from_node, to_node):
            return c[(from_node, to_node)]

        N = [i for i in range(1, n)]
        V = [0] + N
        A = [(i, j) for i in V for j in V]
        #m = 80

        # build initial solution
        source = Node(0, q[0])
        nodes = [Node(i, q[i]) for i in range(1, n)]

        network = Network(source, c, Q)
        network.add_nodes(nodes)

        routes, total_cost = network.build_route()

        # convert vrp route to tsp route
        routes_flattened = [node.id for route in routes for node in route]
        routes_filtered = list(filter(lambda x: x != 0, routes_flattened))

        # build transportation solution to get reduced cost and duals values
        reduced_costs, duals = solve_transportation_problem(N, n, c, q)
        #print(reduced_costs)
        #print(duals)

        # calculate reduced cost for all nodes and arcs
        reduced_costs_matrix = dict()
        for (i, j) in A:
            if i != j:
                reduced_costs_matrix[(i, j)] =  c[(i,j)] - duals[i] - duals[j]

        # check if reduced costs are correct
        for cost in reduced_costs:
            i = cost[0][0]
            j = cost[0][1]
            assert cost[1] == c[(i,j)] - duals[i] - duals[j]
            assert reduced_costs_matrix[(i, j)] == c[(i,j)] - duals[i] - duals[j]

        #print(reduced_costs_matrix)

        # tabu search
        ts = TabuSearch(routes_filtered, reduced_costs_matrix, 20, 15, cost_function, q, Q, N)
        start_time = time.time()
        solution = ts.start(total_cost)
        end_time = time.time() - start_time

        new_value = new_value = {'Instance': result["instance"], 'Paper Obj': result["cost"], 'Our obj': solution["cost"], 'Paper Time': result["time"], 'Our Time': float("{:.2f}".format(end_time)), 'GAP': float("{:.2f}".format(100*solution["cost"]/float(result["cost"])-100))}
        df = df.append(new_value, ignore_index=True)

    print(df)
    print("Time avg:", df["Our Time"].mean())
    print("GAP avg:", df["GAP"].mean())

    #df.to_csv('df.csv')