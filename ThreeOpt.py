from utils import calculate_route_cost

class ThreeOpt:
    def __init__(self, route, cost_function):
        """
        A simple 2-Opt class

            Parameters:
                route: initial route for the 2-opt
                cost_function: a function which calculate the cost between two nodes
        """
        self.route = route
        self.cost_function = cost_function

    def reverse_segment_if_better(self, tour, i, j, k):
        costs = []
        tours = []

        tours.append(tour[:])
        tours.append(tour[:])
        tours.append(tour[:])
        tours.append(tour[:])

        tours[0][i:j] = reversed(tour[i:j])
        tours[1][j:k] = reversed(tour[j:k])
        tours[2][i:k] = reversed(tour[i:k])

        tmp = tour[j:k] + tour[i:j]
        tours[3][i:k] = tmp

        for tour in tours:
            costs.append(calculate_route_cost(self.cost_function, tour))

        min_index = costs.index(min(costs))

        return tours[min_index], costs[min_index]

    def all_segments(self, n):
        return ((i, j, k)
            for i in range(n)
            for j in range(i + 2, n)
            for k in range(j + 2, n + (i > 0)))
    
    def start(self, A, tabu_list):
        swaps = []

        for (a, b, c) in self.all_segments(len(self.route)):
            if  (self.route[a-1], self.route[a]) not in A or (self.route[b-1], self.route[b]) not in A or (self.route[c-1], self.route[c% len(self.route)]) not in A or (self.route[a], self.route[b], self.route[c % len(self.route)]) in tabu_list:
                continue

            new_route, cost = self.reverse_segment_if_better(self.route, a, b, c)

            swaps.append({"move": (self.route[a], self.route[b], self.route[c% len(self.route)]), "route": new_route, "cost": cost})
        
        # order routes using the cost
        return sorted(swaps, key=lambda k: k['cost']) 