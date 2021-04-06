import collections
import math
from SplitRoute import convert_tsp_to_vrp
from TwoOpt import TwoOpt
from ThreeOpt import ThreeOpt
from utils import calculate_route_cost
import bisect

class TabuSearch:
    """
        A simple Tabu Search class

        Attributes:
            initial_solution: initial solution for the tabu method
            reduced_costs: ordered by cost reduced cost of transport problem
            iterations: max number of iterations
            tenure: maximum number of iterations of permanence of a move in the tabu list
            cost_function: a function which calculate the cost between two nodes
            q: demand at nodes
            Q: capacity vehicles
            N: nodes without deposit
    """
    def __init__(self, initial_solution, reduced_costs_arcs, reduced_costs_costs, iterations, tenure, cost_function, q, Q, N):
        """
        Construct a Tabu Search Object

            Parameters:
                initial_solution: initial solution for the tabu method
                reduced_costs_arcs: arcs ordered by reduced cost of transport problem
                reduced_costs_costs: cost ordered by reduced cost of transport problem
                iterations: max number of iterations
                tenure: maximum number of iterations of permanence of a move in the tabu list
                cost_function: a function which calculate the cost between two nodes
                q: demand at nodes
                Q: capacity vehicles
                N: nodes without deposit
        """
        self.initial_solution = initial_solution
        self.reduced_costs_arcs = reduced_costs_arcs
        self.reduced_costs_costs = reduced_costs_costs
        self.iterations = iterations
        self.tenure = tenure
        self.cost_function = cost_function
        self.q = q
        self.Q = Q
        self.N = N

        self.initial_tenure = tenure

        self.A = set()

        # add deposit arcs
        for node in N:
            self.A.add((0, node))
            self.A.add((node, 0))

    def granular(self, N, max_cost):
        """
        Parameters:
            N: nodes without deposit
            max_cost: max reduced cost to consider
        """

        A = set(self.A)

        index_last_reduced_cost = bisect.bisect_right(self.reduced_costs_costs, max_cost)

        # add arcs with reduced costs included in the threshold
        A.update(self.reduced_costs_arcs[0:index_last_reduced_cost])

        return A

    def start(self, initial_cost):
        """
        Start the tabu search

        Parameters:
            initial_cost: initial solution cost
        """

        iteration_number_max = 8
        tenure_increment = 15
        percentage_increment = 0.8
        percentage_decrement = 0.9

        tabu_list = collections.deque(maxlen=self.tenure)
        route = self.initial_solution
        best_route = {"route": self.initial_solution, "cost": initial_cost}
        best_tsp_route = self.initial_solution

        it_count = 0
        best_count = 0

        A = None
        min_cost = self.reduced_costs_costs[0]
        max_cost = min_cost

        max_reduced_cost = self.reduced_costs_costs[-1]

        A = self.granular(self.N, max_cost)

        threeopt = ThreeOpt(self.cost_function, len(route))

        # stop condition
        while self.iterations-it_count > 0:
            if max_cost >= max_reduced_cost:
                #print("Max cost")
                break
            if best_count == iteration_number_max:
                # after iteration_number_max iterations without best solution, augment the granularity
                max_cost = max_cost + abs(max_cost*percentage_increment)
                A = self.granular(self.N, max_cost)
                best_count = 0
                
                # if the number is near 0 we can't increment it using percentages
                if max_cost > -100 and max_cost <= 0:
                    max_cost = 1000

                self.tenure += tenure_increment
                tabu_list = collections.deque(tabu_list, maxlen=self.tenure)

            two_opt_neighborhoods = threeopt.start(route, A, tabu_list)

            if len(two_opt_neighborhoods) != 0:
                best_valid_neighborhood = two_opt_neighborhoods[0]

                tabu_list.append(best_valid_neighborhood["move"])

                # create a feasible route for VRP
                vrp_route = convert_tsp_to_vrp(best_valid_neighborhood["route"], self.q, len(best_valid_neighborhood["route"]), self.Q, self.cost_function)
                vrp_route = list(filter(None, vrp_route))

                vrp_cost = 0
                for trip in vrp_route:
                    vrp_cost += calculate_route_cost(self.cost_function, trip)

                    if vrp_cost > best_route["cost"]:
                        vrp_cost = math.inf
                        break

                if vrp_cost < best_route["cost"]:
                    best_route["route"] = vrp_route
                    best_route["cost"] = vrp_cost
                    route = best_valid_neighborhood["route"]
                    best_tsp_route = best_valid_neighborhood["route"]
                    best_count = 0

                    # decrease granularity
                    max_cost = max_cost - abs(max_cost*percentage_decrement)
                    A = self.granular(self.N, max_cost)
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