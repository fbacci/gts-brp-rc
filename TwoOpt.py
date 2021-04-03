from utils import calculate_route_cost

class TwoOpt:
    def __init__(self, route, cost_function):
        """
        A simple 2-Opt class

            Parameters:
                route: initial route for the 2-opt
                cost_function: a function which calculate the cost between two nodes
        """
        self.route = [0]+route+[0]
        self.cost_function = cost_function

    def _opt_swap(self, route, i, k):
        route_to_i = route[:i]
        route_to_k = list(reversed(route[i:k]))
        route_to_end = route[k:]

        return route_to_i + route_to_k + route_to_end

    def start(self, A, tabu_list):
        swaps = []

        for i in range(1, len(self.route)):
            if (self.route[i-1], self.route[i]) not in A:
                continue

            #print("Old:", self.route)
            for j in range(i+1, len(self.route)):
                if (self.route[j-1], self.route[j]) not in A or (self.route[i], self.route[j]) in tabu_list:
                    continue 
                new_route = self._opt_swap(self.route[:], i, j)

                cost = calculate_route_cost(self.cost_function, new_route[1:-1])

                swaps.append({"move": (self.route[i], self.route[j]), "route": new_route[1:-1], "cost": cost})

        # order routes using the cost
        return sorted(swaps, key=lambda k: k['cost']) 