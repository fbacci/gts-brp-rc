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

def get_cost_adj_partial(new_route, q, Q, cost_function, last_nodes, i, j, old_cost):
    n_vehicles = 1
    local_last_nodes = dict()

    if new_route[0] != 0:
        new_route = [0] + new_route

    if new_route[-1] != 0:
        new_route = new_route + [0]

    cost = cost_function(new_route[-2], 0)
    qp_max = 0
    qp_min = 0
    sum_qp = 0

    first_run = True

    for index, node in enumerate(new_route[1:-1], 1):
        if first_run:
            # first run initialization
            sum_qp = q[node]
            first_run = False
        else:
            sum_qp = sum_qp + q[node]
        
        cost += cost_function(new_route[index-1], node)

        if sum_qp > qp_max:
            qp_max = sum_qp
        
        if sum_qp < qp_min:
            qp_min = sum_qp

        if qp_max - qp_min > Q:
            # return to depot

            # calculate return to depot cost
            cost -= cost_function(new_route[index-1], node) 
            cost += cost_function(new_route[index-1], 0) + cost_function(0, node)

            local_last_nodes[new_route[index-1]] = cost - cost_function(new_route[-2], 0) - cost_function(0, node)

            # reset
            sum_qp = q[node]
            qp_min = 0
            qp_max = 0
            n_vehicles += 1

            if index-1 > i and index-1 > j and new_route[index-1] in last_nodes:
                cost = cost + old_cost - last_nodes.get(new_route[index-1])
                cost -= cost_function(0, node)
                cost -= cost_function(new_route[-2], 0)

                last_nodes_list = list(last_nodes.items())

                prev_node_old_cost = last_nodes.get(new_route[index-1])
                prev_node_new_cost = local_last_nodes.get(new_route[index-1])

                for k,v in last_nodes_list[last_nodes_list.index((new_route[index-1], last_nodes.get(new_route[index-1]))) + 1 :]:
                    local_last_nodes[k] = v - prev_node_old_cost + prev_node_new_cost
                    prev_node_old_cost = last_nodes.get(k)
                    prev_node_new_cost = local_last_nodes.get(k)

                break

    return n_vehicles, cost, local_last_nodes


def get_cost_adj(new_route, q, Q, cost_function, test=0):
    n_vehicles = 1
    last_nodes = dict()

    if new_route[0] != 0:
        new_route = [0] + new_route

    if new_route[-1] != 0:
        new_route = new_route + [0]

    cost_adj = 0
    cost = cost_function(new_route[-2], 0)
    qp_max = 0
    qp_min = 0
    sum_qp = 0

    first_run = True

    for index, node in enumerate(new_route[1:-1], 1):
        if first_run:
            # first run initialization
            sum_qp = q[node]
            first_run = False
        else:
            sum_qp = sum_qp + q[node]
            
        cost += cost_function(new_route[index-1], node)

        if sum_qp > qp_max:
            qp_max = sum_qp
        
        if sum_qp < qp_min:
            qp_min = sum_qp

        if qp_max - qp_min > Q:
            # return to depot

            # calculate return to depot cost
            cost_adj += cost_function(new_route[index-1], 0) + cost_function(0, node)

            cost -= cost_function(new_route[index-1], node)

            last_nodes[new_route[index-1]] = cost + cost_adj - cost_function(new_route[-2], 0) - cost_function(0, node)

            # reset
            sum_qp = q[node]
            qp_min = 0
            qp_max = 0
            n_vehicles += 1

    return n_vehicles, cost, cost_adj, last_nodes

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