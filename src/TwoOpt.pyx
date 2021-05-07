from utils import calculate_route_cost, get_cost_adj
from itertools import accumulate
from SplitRoute import convert_tsp_to_vrp
from operator import itemgetter

cdef class TwoOpt:
    def __init__(self, cost_function):
        """
        A simple 2-Opt class

            Parameters:
                cost_function: a function which calculate the cost between two nodes
        """
        self.cost_function = cost_function

    cdef list _opt_swap(self, list route, int i, int k):
        return route[:i] + list(reversed(route[i:k])) + route[k:]

    cdef list start(self, list route, set A, tabu_list, list q, int Q):
        cdef list swaps = []

        route = [0]+route+[0]

        for i in range(1, len(route)):
            if (route[i-1], route[i]) not in A:
                continue

            for j in range(i+1, len(route)):
                if (route[j-1], route[j]) not in A or (route[i], route[j]) in tabu_list:
                    continue 
                new_route = self._opt_swap(route, i, j)

                n_vehicles, cost, cost_adj, last_nodes = get_cost_adj(new_route, q, Q, self.cost_function)
                cost += cost_adj

                swaps.append({"move": (route[i], route[j]), "route": new_route[1:-1], "cost": cost, "last_nodes": last_nodes})

        # order routes using the cost
        return sorted(swaps, key=itemgetter("cost"))