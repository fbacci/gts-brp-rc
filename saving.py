from itertools import accumulate
import math

def initial_step(N):
    routes = []

    for node in N:
        routes.append([0] + [node] + [0])

    return routes

def check_feasibility(route, q, Q):
    sum_qp = list(accumulate([q[node] for node in route]))
    qp_max = max([0, max(sum_qp)])
    qp_min = min(sum_qp)

    if qp_min > 0:
        qp_min = 0

    return (qp_max - qp_min <= Q)

def merge(savings, routes, k, q, Q):
    max_node_list = []
    current_route = 0
    max_iterations = len(routes)

    while(len(routes) > k and max_iterations > 0):
        i = routes[current_route][1]
        j = routes[current_route][-2]
        savings_route = []


        for index, route in enumerate(routes):
            if index == current_route:
                continue
            # check if h->i route is feasible and save the saving
            h = route[-2]

            new_route = route[0:-1] + routes[current_route][1:]

            if check_feasibility(new_route, q, Q):
                savings_route.append({
                                        "route": index,
                                        "new_route": new_route,
                                        "saving": savings[(h, i)]
                                    })

            # check if j->h route is feasible and save the saving
            h = route[1]

            new_route = routes[current_route][:-1] + route[1:]

            if check_feasibility(new_route, q, Q):
                savings_route.append({
                                        "route": index, 
                                        "new_route": new_route, 
                                        "saving": savings[(j, h)]
                                    })
        
        if len(savings_route) > 0:
            max_node = max(savings_route, key = lambda x: x["saving"])

            max_iterations = len(routes)

            routes[current_route] = max_node["new_route"]
            del routes[max_node["route"]]

            if max_node["route"] < current_route:
                current_route -= 1
        else:
            current_route = (current_route + 1) % len(routes)
            max_iterations -= 1

    return routes

def initial_solution(N, q, Q, cost_function):
    total_q = sum(q)
    min_number_of_vehicles = max(1, math.ceil(abs(total_q)/Q))
    
    savings = {(i, j): cost_function(i, 0) + cost_function(0, j) + cost_function(i, j) for i in N for j in N if i != j}

    routes = initial_step(N)

    routes = merge(savings, routes, min_number_of_vehicles, q, Q)

    return routes