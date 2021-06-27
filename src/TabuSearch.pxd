cdef class TabuSearch:
    cdef readonly list initial_solution
    cdef readonly list reduced_costs_arcs
    cdef readonly list reduced_costs_costs
    cdef readonly int iterations
    cdef readonly dict costs
    cdef int tenure
    cdef readonly list q
    cdef readonly int Q
    cdef readonly list N

    cdef readonly int initial_tenure

    cdef readonly set A

    cdef set granular(self, list N, float max_cost)
    cdef tuple diversification(self, float *max_cost, float percentage_increment, dict best_valid_neighborhood, int *best_count, tabu_list, int tenure_increment)
    cpdef dict start(self, float initial_cost)
