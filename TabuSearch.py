import collections
import math
from SplitRoute import convert_tsp_to_vrp
from TwoOpt import TwoOpt
from utils import calculate_route_cost

class TabuSearch:
    """
        A simple Tabu Search class

        Attributes:
            initial_solution: initial solution for the tabu method
            iterations: max number of iterations
            tenure: maximum number of iterations of permanence of a move in the tabu list
            cost_function: a function which calculate the cost between two nodes
            q: demand at nodes
            Q: capacity vehicles
            N: nodes
    """
    def __init__(self, initial_solution, reduced_costs, iterations, tenure, cost_function, q, Q, N):
        """
        Construct a Tabu Search Object

            Parameters:
                initial_solution: initial solution for the tabu method
                iterations: max number of iterations
                tenure: maximum number of iterations of permanence of a move in the tabu list
                cost_function: a function which calculate the cost between two nodes
                q: demand at nodes
                Q: capacity vehicles
        """
        self.initial_solution = initial_solution
        self.reduced_costs = reduced_costs
        self.iterations = iterations
        self.tenure = tenure
        self.cost_function = cost_function
        self.q = q
        self.Q = Q
        self.N = N

        self.initial_tenure = tenure
    
    def granular(self, N, reduced_costs, max_cost):
        """
        Parameters:
            N: number of nodes
            reduced_costs: reduced costs of arcs
            max_cost: max reduced cost to consider
        """

        A = set()

        # add arcs with reduced costs included in the threshold
        for node1 in N:
            for node2 in N:
                if node1 != node2:
                    current_arc_cost = reduced_costs.get((node1, node2))
                    if current_arc_cost <= max_cost:
                        A.add((node1, node2))

        # add best solution arcs
        for node in N:
            A.add((0, node))
            A.add((node, 0))

        return A

    def start(self, initial_cost):
        """
        Start the tabu search

        Parameters:
            initial_cost: initial solution cost
        """

        iteration_number_max = 20
        tenure_increment = 10

        tabu_list = collections.deque(maxlen=self.tenure)
        route = self.initial_solution
        reduced_costs = self.reduced_costs
        best_route = {"route": self.initial_solution, "cost": initial_cost}
        best_tsp_route = self.initial_solution

        it_count = 0
        best_count = 0

        A = None
        min_cost = reduced_costs[min(reduced_costs.keys(), key=(lambda k: reduced_costs[k]))]
        max_cost = min_cost

        max_reduced_cost = reduced_costs[max(reduced_costs.keys(), key=(lambda k: reduced_costs[k]))]

        A = self.granular(self.N, reduced_costs, max_cost)

        # stop condition
        while self.iterations-it_count > 0:
            if max_cost >= max_reduced_cost:
                print("Max cost")
                break
            if best_count == iteration_number_max:
                # after iteration_number_max iterations without best solution, augment the granularity
                max_cost = max_cost + abs(max_cost*0.8)
                A = self.granular(self.N, reduced_costs, max_cost)
                best_count = 0
                
                # if the number is near 0 we can't increment it using percentuals
                if max_cost > -100 and max_cost <= 0:
                    max_cost = 1000

                self.tenure += tenure_increment
                tabu_list = collections.deque(tabu_list, maxlen=self.tenure)

            two_opt_neighborhoods = TwoOpt(route, self.cost_function).start(A)

            # neighborhood with minimum cost
            best_valid_neighborhood = None

            # find the best neighborhood which doesn't use tabu moves
            for neighborhood in two_opt_neighborhoods:
                if neighborhood["move"] not in tabu_list:
                    best_valid_neighborhood = neighborhood
                    break

            if best_valid_neighborhood is not None:
                tabu_list.append(best_valid_neighborhood["move"])

                # create a feasible route for VRP
                vrp_route = convert_tsp_to_vrp(best_valid_neighborhood["route"], self.q, len(best_valid_neighborhood["route"]), self.Q, self.cost_function)
                vrp_route = list(filter(None, vrp_route))

                vrp_cost = 0
                for trip in vrp_route:
                    vrp_cost += calculate_route_cost(self.cost_function, trip)

                if vrp_cost < best_route["cost"]:
                    best_route["route"] = vrp_route
                    best_route["cost"] = vrp_cost
                    route = best_valid_neighborhood["route"]
                    best_tsp_route = best_valid_neighborhood["route"]
                    best_count = 0

                    # decrease granularity
                    max_cost = max_cost - abs(max_cost*0.9)
                    A = self.granular(self.N, reduced_costs, max_cost)
                    best_count = 0

                    # add best solution arcs to granular
                    for node, next_node in zip(best_valid_neighborhood["route"], best_valid_neighborhood["route"][1:]):
                        A.add((node, next_node))

                    self.tenure -= tenure_increment

                    if self.tenure <= 0:
                        self.tenure = self.initial_tenure

                    tabu_list = collections.deque(tabu_list, maxlen=self.tenure)
                else:
                    best_count += 1

                it_count += 1
            else:
                # if a valid neighborhood is not found, augment the granularity
                best_count = iteration_number_max

        return best_route