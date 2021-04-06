from utils import calculate_route_cost

class ThreeOpt:
    def __init__(self, cost_function, n):
        """
        A simple 2-Opt class

            Parameters:
                cost_function: a function which calculate the cost between two nodes
                n: number of nodes in a route
        """
        self.cost_function = cost_function
        self.all_segments_list = list(self.all_segments(n))

    def all_segments(self, n):
        return ((i, j, k)
            for i in range(n)
            for j in range(i + 2, n)
            for k in range(j + 2, n + (i > 0)))

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
    
    def start(self, route, A, tabu_list):
        swaps = []

        for (a, b, c) in filter(lambda x: not(
                                                (route[x[0]-1], route[x[0]]) not in A 
                                                or (route[x[1]-1], route[x[1]]) not in A
                                                or (route[x[2]-1], route[x[2] % len(route)]) not in A 
                                                or (route[x[0]], route[x[1]], route[x[2] % len(route)]
                                            ) in tabu_list), self.all_segments_list):
  
            new_route, cost = self.reverse_segment_if_better(route, a, b, c)

            swaps.append({"move": (route[a], route[b], route[c% len(route)]), "route": new_route, "cost": cost})

        # order routes using the cost
        return sorted(swaps, key=lambda k: k['cost']) 