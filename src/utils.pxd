cpdef float calculate_route_cost(dict costs, list route)
cdef dict get_cost_adj_partial(list new_route, list q, int Q, dict costs, dict last_nodes, int i, int j, float *old_cost)
cdef dict get_cost_adj(list new_route, list q, int Q, dict costs, float *cost)