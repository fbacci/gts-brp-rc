def calculate_route_cost(cost_function, route):
    """
    Calculate cost of a route
    """

    # Add cost of the delimiters
    cost = cost_function(0, route[0]) + cost_function(route[-1], 0)

    for node, next_node in zip(route, route[1:]):
        cost += cost_function(node, next_node)

    return cost

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