from utils import calculate_route_cost, get_cost_adj, get_cost_adj_partial
from SplitRoute import convert_tsp_to_vrp
from itertools import accumulate
import math

cdef bint DEBUG_COST = False

cdef void check_cost(list route, list q, int Q, float cost2, dict last_nodes2, cost_function):
    cdef float cost
    cdef float cost_adj
    cdef dict last_nodes

    _, cost, cost_adj, last_nodes = get_cost_adj(route, q, Q, cost_function)
    cost += cost_adj

    assert cost == cost2
    assert last_nodes == last_nodes2

cdef dict move(dict best, list q, int Q, cost_function):
    cdef int i
    cdef int j
    cdef list route
    cdef float cost
    cdef dict local_last_nodes
    cdef dict current_best = {"move": None, "route": None, "cost": math.inf, "last_nodes": None}

    for i in range(0, len(best["route"])):
        for j in range(1, len(best["route"])):
            if i == j:
                continue

            route = best["route"][:]
            del route[i]
            route.insert(j-1, best["route"][i])
            
            _, cost, local_last_nodes = get_cost_adj_partial(route, q, Q, cost_function, best["last_nodes"], i+1, j+1, best["cost"])

            if DEBUG_COST:
                check_cost(route, q, Q, cost, local_last_nodes, cost_function)

            if cost < current_best["cost"]:
                current_best = {"move": None, "route": route, "cost": cost, "last_nodes": local_last_nodes}
    
    return current_best

cdef dict move_2_reverse(dict best, list q, int Q, cost_function):
    cdef dict current_best = {"move": None, "route": None, "cost": math.inf, "last_nodes": None}
    cdef int i
    cdef int j
    cdef list route
    cdef float cost
    cdef dict local_last_nodes
    
    for i in range(0, len(best["route"]) -2):
        for j in range(1, len(best["route"]) -1):
            if i == j:
                continue

            route = best["route"][:]

            del route[i]  # i
            del route[i]  # i+1

            route.insert(j-1, best["route"][i+1])
            route.insert(j, best["route"][i])

            _, cost, local_last_nodes = get_cost_adj_partial(route, q, Q, cost_function, best["last_nodes"], i+2, j+1, best["cost"])

            if DEBUG_COST:
                check_cost(route, q, Q, cost, local_last_nodes, cost_function)

            if cost < current_best["cost"]:
                current_best = {"move": None, "route": route, "cost": cost, "last_nodes": local_last_nodes}

    return current_best

cdef dict swap_1_1(dict best, list q, int Q, cost_function):
    cdef int i
    cdef int j
    cdef list route
    cdef float cost
    cdef dict local_last_nodes
    cdef dict current_best = {"move": None, "route": None, "cost": math.inf, "last_nodes": None}

    for i in range(0, len(best["route"])):
        for j in range(i+1, len(best["route"])):
            route = best["route"][:]
            route[i], route[j] = route[j], route[i]
            
            _, cost, local_last_nodes = get_cost_adj_partial(route, q, Q, cost_function, best["last_nodes"], i+1, j+1, best["cost"])
            
            if DEBUG_COST:
                check_cost(route, q, Q, cost, local_last_nodes, cost_function)

            if cost < current_best["cost"]:
                current_best = {"move": None, "route": route, "cost": cost, "last_nodes": local_last_nodes}

    return current_best

cdef dict swap_2_2(dict best, list q, int Q, cost_function):
    cdef int i
    cdef int j
    cdef list route
    cdef list swap
    cdef float cost
    cdef dict local_last_nodes
    cdef dict current_best = {"move": None, "route": None, "cost": math.inf, "last_nodes": None}

    for i in range(0, len(best["route"])):
        for j in range(2+i, len(best["route"])-1):
            route = best["route"][:]
            swap = route[i:i+2]
            route[i:i+2]=  route[j:j+2]
            route[j:j+2] = swap

            _, cost, local_last_nodes = get_cost_adj_partial(route, q, Q, cost_function, best["last_nodes"], i+2, j+2, best["cost"])
            
            if DEBUG_COST:
                check_cost(route, q, Q, cost, local_last_nodes, cost_function)

            if cost < current_best["cost"]:
                current_best = {"move": None, "route": route, "cost": cost, "last_nodes": local_last_nodes}
            #best_list.append({"move": None, "route": route, "cost": cost, "last_nodes": local_last_nodes})


    return current_best

cdef dict swap_3_3_reversed(dict best, list q, int Q, cost_function):
    cdef int i
    cdef int j
    cdef list route
    cdef list swap
    cdef float cost
    cdef dict local_last_nodes
    cdef dict current_best = {"move": None, "route": None, "cost": math.inf, "last_nodes": None}

    for i in range(0, len(best["route"])):
        for j in range(3+i, len(best["route"])-2):
            route = best["route"][:]
            swap = route[i:i+3]
            route[i:i+3]=  route[j:j+3]
            route[j:j+3] = reversed(swap)

            _, cost, local_last_nodes = get_cost_adj_partial(route, q, Q, cost_function, best["last_nodes"], i+3, j+3, best["cost"])
            
            if DEBUG_COST:
                check_cost(route, q, Q, cost, local_last_nodes, cost_function)

            if cost < current_best["cost"]:
                current_best = {"move": None, "route": route, "cost": cost, "last_nodes": local_last_nodes}
            #best_list.append({"move": None, "route": route, "cost": cost, "last_nodes": local_last_nodes})
    
    return current_best

cdef dict swap_3_3(dict best, list q, int Q, cost_function):
    cdef int i
    cdef int j
    cdef list route
    cdef list swap
    cdef float cost
    cdef dict local_last_nodes
    cdef dict current_best = {"move": None, "route": None, "cost": math.inf, "last_nodes": None}

    for i in range(0, len(best["route"])):
        for j in range(3+i, len(best["route"])-2):
            route = best["route"][:]
            swap = route[i:i+3]
            route[i:i+3]=  route[j:j+3]
            route[j:j+3] = swap

            _, cost, local_last_nodes = get_cost_adj_partial(route, q, Q, cost_function, best["last_nodes"], i+3, j+3, best["cost"])
            
            if DEBUG_COST:
                check_cost(route, q, Q, cost, local_last_nodes, cost_function)
            
            if cost < current_best["cost"]:
                current_best = {"move": None, "route": route, "cost": cost, "last_nodes": local_last_nodes}

    return current_best
