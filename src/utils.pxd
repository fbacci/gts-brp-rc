cpdef float calculate_route_cost(cost_function, list route)
cdef dict get_cost_adj_partial(list new_route, list q, int Q, cost_function, dict last_nodes, int i, int j, float *old_cost)
cdef dict get_cost_adj(list new_route, list q, int Q, cost_function, float *cost)