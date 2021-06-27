from itertools import islice
from SplitRoute cimport convert_tsp_to_vrp

cpdef float calculate_route_cost(dict costs, list route):
    """
    Calculate cost of a route
    """

    # Add cost of the delimiters
    cdef float cost = costs[0, route[0]] + costs[route[-1], 0]
    cdef int node
    cdef int next_node

    for node, next_node in zip(route, islice(route, 1, None)):
        cost += costs[node, next_node]

    return cost

cdef dict get_cost_adj_partial(list new_route, list q, int Q, dict costs, dict last_nodes, int i, int j, float *old_cost):
    cdef int n_vehicles = 1
    cdef dict local_last_nodes = dict()

    if new_route[0] != 0:
        new_route = [0] + new_route

    if new_route[-1] != 0:
        new_route = new_route + [0]

    cdef float cost = costs[new_route[-2], 0]
    cdef int qp_max = 0
    cdef int qp_min = 0
    cdef int sum_qp = 0

    cdef bint first_run = True

    cdef int index
    cdef int node

    for index, node in enumerate(new_route[1:-1], 1):
        if first_run:
            # first run initialization
            sum_qp = q[node]
            first_run = False
        else:
            sum_qp = sum_qp + q[node]
        
        cost += costs[new_route[index-1], node]

        if sum_qp > qp_max:
            qp_max = sum_qp
        
        if sum_qp < qp_min:
            qp_min = sum_qp

        if qp_max - qp_min > Q:
            # return to depot

            # calculate return to depot cost
            cost -= costs[new_route[index-1], node]
            cost += costs[new_route[index-1], 0] + costs[0, node]

            local_last_nodes[new_route[index-1]] = cost - costs[new_route[-2], 0] - costs[0, node]

            # reset
            sum_qp = q[node]
            qp_min = 0
            qp_max = 0
            n_vehicles += 1

            if index-1 > i and index-1 > j and new_route[index-1] in last_nodes:
                cost = cost + old_cost[0] - last_nodes.get(new_route[index-1])
                cost -= costs[0, node]
                cost -= costs[new_route[-2], 0]

                last_nodes_list = list(last_nodes.items())

                prev_node_old_cost = last_nodes.get(new_route[index-1])
                prev_node_new_cost = local_last_nodes.get(new_route[index-1])

                for k,v in last_nodes_list[last_nodes_list.index((new_route[index-1], last_nodes.get(new_route[index-1]))) + 1 :]:
                    local_last_nodes[k] = v - prev_node_old_cost + prev_node_new_cost
                    prev_node_old_cost = last_nodes.get(k)
                    prev_node_new_cost = local_last_nodes.get(k)

                break

    old_cost[0] = cost
    return local_last_nodes

cdef dict get_cost_adj(list new_route, list q, int Q, dict costs, float *cost):
    cdef int n_vehicles = 1
    cdef dict last_nodes = dict()

    if new_route[0] != 0:
        new_route = [0] + new_route

    if new_route[-1] != 0:
        new_route = new_route + [0]

    cdef float cost_adj = 0
    cdef int qp_max = 0
    cdef int qp_min = 0
    cdef int sum_qp = 0

    cdef bint first_run = True
    cdef int index
    cdef int node

    cost[0] = costs[new_route[-2], 0]

    for index, node in enumerate(new_route[1:-1], 1):
        if first_run:
            # first run initialization
            sum_qp = q[node]
            first_run = False
        else:
            sum_qp = sum_qp + q[node]
            
        cost[0] += costs[new_route[index-1], node]

        if sum_qp > qp_max:
            qp_max = sum_qp
        
        if sum_qp < qp_min:
            qp_min = sum_qp

        if qp_max - qp_min > Q:
            # return to depot

            # calculate return to depot cost
            cost_adj += costs[new_route[index-1], 0] + costs[0, node]

            cost[0] -= costs[new_route[index-1], node]

            last_nodes[new_route[index-1]] = cost[0] + cost_adj - costs[new_route[-2], 0]- costs[0, node]

            # reset
            sum_qp = q[node]
            qp_min = 0
            qp_max = 0
            n_vehicles += 1


    cost[0] += cost_adj
    return last_nodes

cdef float get_cost_prins(list route, list q, int route_size, int Q, dict costs):
    cdef float cost = 0
    routes = convert_tsp_to_vrp(route, q, route_size, Q, costs)
    routes = list(filter(None, routes))

    for route2 in routes:
        cost += calculate_route_cost(costs, route2)

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