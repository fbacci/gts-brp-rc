from utils import calculate_route_cost, get_cost_adj
from itertools import accumulate
from SplitRoute import convert_tsp_to_vrp
from operator import itemgetter

class TwoOpt:
    def __init__(self, cost_function):
        """
        A simple 2-Opt class

            Parameters:
                cost_function: a function which calculate the cost between two nodes
        """
        self.cost_function = cost_function

    def _opt_swap(self, route, i, k):
        route_to_i = route[:i]
        route_to_k = list(reversed(route[i:k]))
        route_to_end = route[k:]

        return route_to_i + route_to_k + route_to_end

    def start(self, route, A, tabu_list, q, Q):
        swaps = []

        route = [0]+route+[0]
        sumq = abs(sum([abs(c) for c in q]))

        for i in range(1, len(route)):
            if (route[i-1], route[i]) not in A:
                continue

            for j in range(i+1, len(route)):
                if (route[j-1], route[j]) not in A or (route[i], route[j]) in tabu_list:
                    continue 
                new_route = self._opt_swap(route, i, j)

                #vrp_route = convert_tsp_to_vrp(new_route[1:-1], q, len(new_route[1:-1]), Q, self.cost_function) 
                #vrp_route = list(filter(None, vrp_route)) 
            
            
                #vrp_cost = 0 
                #for trip in vrp_route: 
                #    vrp_cost += calculate_route_cost(self.cost_function, trip) 
                vrp_cost = None
                vrp_route = None

                cost = calculate_route_cost(self.cost_function, new_route[1:-1])

                n_vehicles, cost_adj = get_cost_adj(new_route, q, Q, self.cost_function)

                #assert n_vehicles <= len(vrp_route)

                cost += cost_adj

                swaps.append({"move": (route[i], route[j]), "route": new_route[1:-1], "cost": cost, "n_vehicles": n_vehicles, "vrp_cost": vrp_cost, "vrp_route": vrp_route})

        # order routes using the cost
        sorte = sorted(swaps, key=itemgetter("n_vehicles", "cost"))

        #if len(sorte) > 0:
        #    mino = min(sorte, key=lambda x: x["vrp_cost"])
        #
        #    if mino != sorte[0]:
        #        print(sorte.index(mino))
        #        print("bla")
        return sorte