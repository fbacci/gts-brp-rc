import math

cdef list split(list S, list q, int n, int W, list d, float L, dict costs):
    """
        Parameters:
            S: TSP route to convert
            q: demand at nodes
            n: number of nodes
            W: capacity of vehicle
            d: cost to visit a node (0 if vrp)
            L: maximum route cost (infinity inf vrp)
            costs: costs dict
    """

    cdef int i
    cdef int j

    cdef list V = []
    cdef list P

    cdef int cost
    cdef list P_dup
    cdef list sum_qp

    cdef int qp_max
    cdef int qp_min

    V.append(0)

    for i in range(1, n+1):
        V.append(math.inf)

    P = []

    for i in range(n+1):
        P.append(0)
    
    for i in range(1, n+1):
        cost = 0
        j = i
        P_dup = [0]
        sum_qp = []

        while True:
            P_dup.append(S[j])

            # cumulative sum
            if len(sum_qp) == 0:
                sum_qp.append(q[P_dup[-1]])
            else:
                sum_qp.append(sum_qp[-1] + q[P_dup[-1]])

            qp_max = max([0, max(sum_qp)])
            qp_min = min(sum_qp)

            if qp_min > 0:
                qp_min = 0

            if i == j:
                cost = costs[0, S[j]] + d[S[j]] + costs[S[j], 0]
            else:
                cost = cost - costs[S[j-1], 0] + costs[S[j-1], S[j]] + d[S[j]] + costs[S[j], 0]

            if (cost <= L) and (qp_max - qp_min <= W):
                if V[i-1]+cost < V[j]:
                    V[j] = V[i-1]+cost
                    P[j] = i-1

                j += 1
            if (j > n) or (cost > L) or (qp_max - qp_min > W):
                break
    return P

cdef list extract_vrp(int n, list S, list P):
    cdef list trip = []
    cdef int t
    cdef int i
    cdef int j

    for _ in range(1, n+1):
        trip.append([])

    t = 0
    j = n

    while True:
        i = P[j]

        for k in range(i+1, j+1):
            trip[t].append(S[k])

        j = i

        t += 1
        if i == 0:
            break

    return trip

cdef list convert_tsp_to_vrp(list S, list q, int n, int W, dict costs):
    """
        Parameters:
            S: TSP route to convert
            q: demand at nodes
            n: number of nodes
            W: capacity of vehicle
            costs: cost dict
            d: cost to visit a node (0 if vrp)
            L: maximum route cost (infinity inf vrp)
    """

    cdef list P
    cdef d=None
    cdef L=math.inf

    if d is None:
        d = [0 for _ in range(n+1)]

    P = split([0]+S, q, n, W, d, L, costs)

    return extract_vrp(n, [0]+S, P)
