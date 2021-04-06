from utils import calculate_route_cost

class ThreeOpt:
    def __init__(self, cost_function):
        """
        A simple 2-Opt class

            Parameters:
                cost_function: a function which calculate the cost between two nodes
        """
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

        tours[3][i:k] = tour[j:k] + tour[i:j]

        for tour in tours:
            costs.append(calculate_route_cost(self.cost_function, tour[1:-1]))

        min_index = costs.index(min(costs))

        return tours[min_index], costs[min_index]
    
    def start(self, route, A, tabu_list):
        swaps = []

        route = [0]+route+[0]

        n = len(route)
        
        for i in range(1, n):
            if (route[i-1], route[i]) not in A:
                continue
            for j in range(i + 1, n):
                if (route[j-1], route[j]) not in A:
                    continue
                for k in range(j + 1, n):
                    if (route[k-1], route[k]) not in A or (route[i], route[j], route[k]) in tabu_list:
                        continue
  
                    new_route, cost = self.reverse_segment_if_better(route, i, j, k)

                    swaps.append({"move": (route[i], route[j], route[k]), "route": new_route[1:-1], "cost": cost})

        # order routes using the cost
        return sorted(swaps, key=lambda k: k['cost']) 