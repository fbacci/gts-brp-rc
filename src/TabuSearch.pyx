import collections
import math
from SplitRoute cimport convert_tsp_to_vrp
from TwoOpt cimport TwoOpt
from LocalSearch cimport move, move_2_reverse, swap_1_1, swap_2_2, swap_3_3_reversed, swap_3_3
from utils cimport calculate_route_cost
import bisect
from itertools import islice

cdef class TabuSearch:
    """
        A simple Tabu Search class

        Attributes:
            initial_solution: initial solution for the tabu method
            reduced_costs: ordered by cost reduced cost of transport problem
            iterations: max number of iterations
            tenure: maximum number of iterations of permanence of a move in the tabu list
            costs: cost dict
            q: demand at nodes
            Q: capacity vehicles
            N: nodes without deposit
    """
    def __init__(self, initial_solution, reduced_costs_arcs, reduced_costs_costs, iterations, tenure, costs, q, Q, N):
        """
        Construct a Tabu Search Object

            Parameters:
                initial_solution: initial solution for the tabu method
                reduced_costs_arcs: arcs ordered by reduced cost of transport problem
                reduced_costs_costs: cost ordered by reduced cost of transport problem
                iterations: max number of iterations
                tenure: maximum number of iterations of permanence of a move in the tabu list
                costs: cost dict
                q: demand at nodes
                Q: capacity vehicles
                N: nodes without deposit
        """
        self.initial_solution = initial_solution
        self.reduced_costs_arcs = reduced_costs_arcs
        self.reduced_costs_costs = reduced_costs_costs
        self.iterations = iterations
        self.tenure = tenure
        self.costs = costs
        self.q = q
        self.Q = Q
        self.N = N

        self.initial_tenure = tenure

        self.A = set()

        # add deposit arcs
        for node in N:
            self.A.add((0, node))
            self.A.add((node, 0))
            

        self.used_arcs = [[0 for _ in range(len(self.N)+1)] for _ in range(len(self.N)+1)]
        self.used_arcs_number = 0

    cdef set granular(self, list N, float max_cost, list used_arcs_frequency = None):
        """
        Parameters:
            N: nodes without deposit
            max_cost: max reduced cost to consider
        """

        cdef set A = set(self.A)

        #index_last_reduced_cost = bisect.bisect_right(self.reduced_costs_costs, max_cost)

        # add arcs with reduced costs included in the threshold
        #A.update(self.reduced_costs_arcs[0:index_last_reduced_cost])

        cdef dict rc = {}

        if self.used_arcs_number > 0 and used_arcs_frequency != None:
            for i in range(len(self.reduced_costs_costs)):
                if self.reduced_costs_costs[i] >= 0:
                    rc[self.reduced_costs_arcs[i]] = self.reduced_costs_costs[i] - 0.3*(self.reduced_costs_costs[i] * 1/(0.1+used_arcs_frequency[self.reduced_costs_arcs[i][0]][self.reduced_costs_arcs[i][1]]))
                else:
                    rc[self.reduced_costs_arcs[i]] = self.reduced_costs_costs[i] + 0.45*(self.reduced_costs_costs[i] * 1/(0.1+used_arcs_frequency[self.reduced_costs_arcs[i][0]][self.reduced_costs_arcs[i][1]]))
                    
                A.update([k for k, v in rc.items() if v <= max_cost])
        else:
            index_last_reduced_cost = bisect.bisect_right(self.reduced_costs_costs, max_cost)
            A.update(self.reduced_costs_arcs[0:index_last_reduced_cost])

        return A

    cdef tuple diversification(self, float *max_cost, float percentage_increment, dict best_valid_neighborhood, int *best_count, tabu_list, int tenure_increment):
        """
        Diversification step

        """

        # calculate arcs frequency
        if self.used_arcs_number > 0:
            used_arcs_frequency = [[self.used_arcs[i][j]/self.used_arcs_number for i in range(len(self.N)+1)] for j in range(len(self.N)+1)]
        else:
            used_arcs_frequency = []

        # after iteration_number_max iterations without best solution, augment the granularity
        max_cost[0] = max_cost[0] + abs(max_cost[0]*percentage_increment)

        # if the number is near 0 we can't increment it using percentages
        if max_cost[0] > -100 and max_cost[0] <= 0:
            max_cost[0] = 1000

        A = self.granular(self.N, max_cost[0], used_arcs_frequency)

        best_count[0] = 0

        self.tenure += tenure_increment
        
        tabu_list = collections.deque(tabu_list, maxlen=self.tenure)
        
        best_valid_neighborhood = move_2_reverse(best_valid_neighborhood, self.q, self.Q, self.costs)
        best_valid_neighborhood = swap_3_3_reversed(best_valid_neighborhood, self.q, self.Q, self.costs)
        best_valid_neighborhood = swap_3_3(best_valid_neighborhood, self.q, self.Q, self.costs)
        best_valid_neighborhood = swap_2_2(best_valid_neighborhood, self.q, self.Q, self.costs)
        best_valid_neighborhood = swap_1_1(best_valid_neighborhood, self.q, self.Q, self.costs)
        best_valid_neighborhood = move(best_valid_neighborhood, self.q, self.Q, self.costs)
        return best_valid_neighborhood, A, tabu_list

    cpdef dict start(self, float initial_cost):
        """
        Start the tabu search

        Parameters:
            initial_cost: initial solution cost
        """

        cdef int iteration_number_max = 18
        cdef int tenure_increment = 7
        cdef float percentage_increment = 0.1
        cdef float percentage_decrement = 0.2

        cdef list trip

        tabu_list = collections.deque(maxlen=self.tenure)
        cdef list route = self.initial_solution
        cdef dict best_route = {"route": self.initial_solution, "cost": initial_cost}
        cdef dict best_valid_neighborhood = {"move": None, "route": self.initial_solution, "cost": initial_cost, "last_nodes": None}
        cdef dict best_tsp_route = best_valid_neighborhood

        cdef int it_count = 0
        cdef int best_count = 0

        cdef float min_cost = self.reduced_costs_costs[0]
        cdef float max_cost = min_cost

        cdef float max_reduced_cost = self.reduced_costs_costs[-1]

        cdef set A = self.granular(self.N, max_cost)

        opt = TwoOpt(self.costs)

        cdef list solutions = [{"iteration": -1, "f obj": initial_cost, "best": True}]

        cdef list two_opt_neighborhoods

        cdef list vrp_route
        cdef float vrp_cost

        # stop condition
        while self.iterations-it_count > 0:
            if max_cost >= max_reduced_cost:
                break
            if best_count >= iteration_number_max:
                best_valid_neighborhood, A, tabu_list = self.diversification(&max_cost, percentage_increment, best_valid_neighborhood, &best_count, tabu_list, tenure_increment)
                two_opt_neighborhoods = [best_valid_neighborhood]
            else:
                two_opt_neighborhoods = opt.start(route, A, tabu_list, self.q, self.Q)

            if len(two_opt_neighborhoods) > 0:
                best_valid_neighborhood = two_opt_neighborhoods[0]

                tabu_list.append(best_valid_neighborhood["move"])

                # create a feasible route for VRP
                vrp_route = convert_tsp_to_vrp(best_valid_neighborhood["route"], self.q, len(best_valid_neighborhood["route"]), self.Q, self.costs)
                vrp_route = list(filter(None, vrp_route))

                vrp_cost = 0
                for trip in vrp_route:
                    vrp_cost += calculate_route_cost(self.costs, trip)

                    if vrp_cost > best_route["cost"]:
                        break

                solutions.append({"iteration": it_count, "f obj": vrp_cost, "best": False})

                if vrp_cost < best_route["cost"]:
                    # update used arcs
                    for node, next_node in zip(best_valid_neighborhood["route"], islice(best_valid_neighborhood["route"], 1, None)):
                        self.used_arcs[node][next_node] = self.used_arcs[node][next_node] + 1
                        self.used_arcs_number = self.used_arcs_number + 1

                    # New best solution found
                    solutions[-1]["best"] = True

                    best_route["route"] = vrp_route
                    best_route["cost"] = vrp_cost
                    route = best_valid_neighborhood["route"]
                    best_tsp_route = best_valid_neighborhood
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

            else:
                # if a valid neighborhood is not found, diversificate
                best_count = iteration_number_max

            it_count += 1
        return best_route
        #, solutions