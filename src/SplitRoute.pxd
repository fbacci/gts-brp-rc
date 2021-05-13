cdef list split(list S, list q, int n, int W, list d, float L, dict costs)
cdef list extract_vrp(int n, list S, list P)
cdef list convert_tsp_to_vrp(list S, list q, int n, int W, dict costs)