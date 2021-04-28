from itertools import islice

def calculate_route_cost(cost_function, route):
    """
    Calculate cost of a route
    """

    # Add cost of the delimiters
    cost = cost_function(0, route[0]) + cost_function(route[-1], 0)

    for node, next_node in zip(route, islice(route, 1, None)):
        cost += cost_function(node, next_node)

    return cost

def get_cost_adj(new_route, q, Q, cost_function):
    qp = []
    n_vehicles = 1
    cost_adj = 0
    qp_max = 0
    qp_min = 0
    sum_qp = 0

    for index, node in enumerate(new_route[1:-1], 1):
        if len(qp) > 0:
            sum_qp = sum_qp + q[node]
        else:
            sum_qp = q[node]

        qp.append(q[node])

        if sum_qp > qp_max:
            qp_max = sum_qp
        
        if sum_qp < qp_min:
            qp_min = sum_qp

        if qp_max - qp_min > Q:
            cost_adj += cost_function(new_route[index-1], 0) + cost_function(0, node)
            qp = [q[node]]
            sum_qp = q[node]
            qp_min = 0
            qp_max = 0
            n_vehicles += 1

    return n_vehicles, cost_adj

def open_dataset(file):
    dataset = open(file, "r")

    i = 0

    while True:
        line = dataset.readline()

        if not line:
            break

        if(i == 0):
            n_nodes = int(line)
            costs = {(i, j): 0 for i in range(n_nodes) for j in range(n_nodes)}
        elif(i == 1):
            q_vertices = [int(q) for q in line.split()]
        elif(i == 2):
            c_vehicles = int(line)
        else:
            j = 0
            for el in line.split():
                costs[(i-3, j)] = float(el)
                j = j+1

        i = i+1

    dataset.close()

    return (n_nodes, costs, q_vertices, c_vehicles)

def open_results(results_file):
    results = []

    for r in results_file:
        result_row = {}
        splitted = r.split(" ")
        result_row["instance"] = splitted[0]
        result_row["cost"] = splitted[1]
        result_row["time"] = splitted[2]

        results.append(result_row)

    return results