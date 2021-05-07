cdef class TwoOpt:
    cdef readonly cost_function

    cdef list _opt_swap(self, list route, int i, int k)
    cdef list start(self, list route, set A, tabu_list, list q, int Q)