from utils import calculate_route_cost

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

    def start(self, route, A, tabu_list):
        swaps = []

        route = [0]+route+[0]

        for i in range(1, len(route)):
            if (route[i-1], route[i]) not in A:
                continue

            for j in range(i+1, len(route)):
                if (route[j-1], route[j]) not in A or (route[i], route[j]) in tabu_list:
                    continue 
                new_route = self._opt_swap(route, i, j)

                cost = calculate_route_cost(self.cost_function, new_route[1:-1])

                swaps.append({"move": (route[i], route[j]), "route": new_route[1:-1], "cost": cost})

        # order routes using the cost
        return sorted(swaps, key=lambda k: k['cost']) 