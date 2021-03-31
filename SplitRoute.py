import math

def split(S, q, n, W, d, L, cost_function):
    """
        Parameters:
            S: TSP route to convert
            q: demand at nodes
            n: number of nodes
            W: capacity of vehicle
            d: cost to visit a node (0 if vrp)
            L: maximum route cost (infinity inf vrp)
            cost_function: a function which calculate the cost between two nodes
    """
    V = []
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

        while True:
            P_dup.append(S[j])

            sum_qp = [sum([q[p] for p in P_dup[1:i+1]]) for i, _ in enumerate(P_dup[1:], start=1)]
            qp_max = max([0, max(sum_qp)])
            qp_min = min(sum_qp)

            if qp_min > 0:
                qp_min = 0

            if i == j:
                cost = cost_function(0, S[j]) + d[S[j]] + cost_function(S[j], 0)
            else:
                cost = cost - cost_function(S[j-1], 0) + cost_function(S[j-1], S[j]) + d[S[j]] + cost_function(S[j], 0)

            if (cost <= L) and (qp_max - qp_min <= W):
                if V[i-1]+cost < V[j]:
                    V[j] = V[i-1]+cost
                    P[j] = i-1

                j += 1
            if (j > n) or (cost > L) or (qp_max - qp_min > W):
                break
    return P

def extract_vrp(n, S, P):
    trip = []

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

def convert_tsp_to_vrp(S, q, n, W, cost_function, d=None, L=math.inf):
    """
        Parameters:
            S: TSP route to convert
            q: demand at nodes
            n: number of nodes
            W: capacity of vehicle
            cost_function: a function which calculate the cost between two nodes
            d: cost to visit a node (0 if vrp)
            L: maximum route cost (infinity inf vrp)
    """


    if d is None:
        d = [0 for _ in range(n+1)]

    P = split([0]+S, q, n, W, d, L, cost_function)

    return extract_vrp(n, [0]+S, P)
