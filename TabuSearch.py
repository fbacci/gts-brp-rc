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
    
    def granular(self, N, reduced_costs, min_cost, max_cost, K=1):
        """
        Parameters:
            beta: sparsification parameter
            z: a solution value
            n: number of nodes
            best_solution: best solution route
            K: number of vehicles (1 in TSP)
            reduced_costs: reduced costs of arcs
            increase_percentage: percentage of threshold increase
        """

        A = set()

        # add arcs with reduced costs included in the threshold
        for node1 in N:
            for node2 in N:
                if node1 != node2:
                    current_arc_cost = reduced_costs.get((node1, node2))
                    if current_arc_cost >= min_cost and current_arc_cost <= max_cost:
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

        tabu_list = collections.deque(maxlen=self.tenure)
        route = self.initial_solution
        reduced_costs = self.reduced_costs
        best_route = {"route": self.initial_solution, "cost": initial_cost}
        best_tsp_route = self.initial_solution
        it_count = 0
        best_count = 0
        A = None
        #increase_percentage = 10
        min_cost = reduced_costs[min(reduced_costs.keys(), key=(lambda k: reduced_costs[k]))]
        max_cost = -2000

        A = self.granular(self.N, reduced_costs, min_cost, max_cost)

        # stop condition
        while self.iterations-it_count > 0:
            # re-create granular from scratch each 2*n iterations
            if best_count == 5:
                max_cost += 500
                A = self.granular(self.N, reduced_costs, min_cost, max_cost)
                best_count = 0

            two_opt_neighborhoods = TwoOpt(route, self.cost_function).start(A)

            # neighborhood with minimum cost
            best_valid_neighborhood = None

            #print(two_opt_neighborhoods)

            # find the best neighborhood which doesn't use tabu moves
            for neighborhood in two_opt_neighborhoods:
                if neighborhood["move"] not in tabu_list:
                    best_valid_neighborhood = neighborhood
                    break

            if best_valid_neighborhood is None:
                raise ValueError("Valid neighborhood not found")

            tabu_list.append(best_valid_neighborhood["move"])

            # add current solution arcs to granular
            for node, next_node in zip(best_valid_neighborhood["route"], best_valid_neighborhood["route"][1:]):
                A.add((node, next_node))

            #print("Best valid: ", best_valid_neighborhood["route"])

            # create a feasible route for VRP
            vrp_route = convert_tsp_to_vrp(best_valid_neighborhood["route"], self.q, len(best_valid_neighborhood["route"]), self.Q, self.cost_function)
            vrp_route = list(filter(None, vrp_route))

            vrp_cost = 0
            for trip in vrp_route:
                vrp_cost += calculate_route_cost(self.cost_function, trip)

            #print("New route:", vrp_route, vrp_cost)

            if vrp_cost < best_route["cost"]:
                best_route["route"] = vrp_route
                best_route["cost"] = vrp_cost
                route = best_valid_neighborhood["route"]
                best_tsp_route = route
                best_count = 0
            else:
                best_count += 1

            it_count += 1

        return best_route