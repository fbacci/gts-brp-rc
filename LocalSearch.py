from utils import calculate_route_cost
from SplitRoute import convert_tsp_to_vrp
from itertools import accumulate

def count_vehicle(new_route, q, Q):
    sum_q = 0
    n_vehicles = 1

    for node in new_route:
        sum_q += q[node]

        if sum_q > Q:
            sum_q = q[node]
            n_vehicles += 1

    return n_vehicles

def move(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(0, len(best["route"])):
            route = best["route"][:]
            del route[i]
            route.insert(j, best["route"][i])

            cost = calculate_route_cost(cost_function, route)
            n_vehicles = count_vehicle(route, q, Q)

            if best["n_vehicles"] > n_vehicles and best["cost"] > cost:
                best_list.append({"move": None, "route": route, "cost": cost, "n_vehicles": n_vehicles})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: (x["n_vehicles"], x["cost"]))    
    return sorto[0]

def move_2_reverse(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"]) -2):
        for j in range(0, len(best["route"]) -1):
            route = best["route"][:]

            del route[i]  # i
            del route[i]  # i+1

            route.insert(j, best["route"][i+1])
            route.insert(j+1, best["route"][i])

            cost = calculate_route_cost(cost_function, route)
            n_vehicles = count_vehicle(route, q, Q)

    if best["n_vehicles"] > n_vehicles and best["cost"] > cost:
                best_list.append({"move": None, "route": route, "cost": cost, "n_vehicles": n_vehicles})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: (x["n_vehicles"], x["cost"]))    

    return sorto[0]

def swap_1_1(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(i+1, len(best["route"])):
            route = best["route"][:]
            route[i], route[j] = route[j], route[i]

            cost = calculate_route_cost(cost_function, route)
            n_vehicles = count_vehicle(route, q, Q)

    if best["n_vehicles"] > n_vehicles and best["cost"] > cost:
                best_list.append({"move": None, "route": route, "cost": cost, "n_vehicles": n_vehicles})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: (x["n_vehicles"], x["cost"]))    

    return sorto[0]

def swap_2_2(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(2+i, len(best["route"])-1):
            route = best["route"][:]
            swap = route[i:i+2]
            route[i:i+2]=  route[j:j+2]
            route[j:j+2] = swap

            cost = calculate_route_cost(cost_function, route)
            n_vehicles = count_vehicle(route, q, Q)

    if best["n_vehicles"] > n_vehicles and best["cost"] > cost:
                best_list.append({"move": None, "route": route, "cost": cost, "n_vehicles": n_vehicles})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: (x["n_vehicles"], x["cost"]))    

    return sorto[0]

def swap_1_1_1(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(i+1, len(best["route"])):
            for k in range(j+1, len(best["route"])):
                route = best["route"][:]

                route[i], route[j], route[k] = route[j], route[k], route[i]

                cost = calculate_route_cost(cost_function, route)
                n_vehicles = count_vehicle(route, q, Q)

                if cost < best["cost"]:
                    best_list.append({"move": None, "route": route, "cost": cost})
                
                route[i], route[j], route[k] = route[k], route[i], route[j]

                cost = calculate_route_cost(cost_function, route)
                n_vehicles = count_vehicle(route, q, Q)

                if cost < best["cost"]:
                    best_list.append({"move": None, "route": route, "cost": cost})          

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: (x["n_vehicles"], x["cost"]))    

    return sorto[0]

def swap_3_3_reversed(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(3+i, len(best["route"])-2):
            route = best["route"][:]
            swap = route[i:i+3]
            route[i:i+3]=  route[j:j+3]
            route[j:j+3] = reversed(swap)

            cost = calculate_route_cost(cost_function, route)
            n_vehicles = count_vehicle(route, q, Q)

            if best["n_vehicles"] > n_vehicles and best["cost"] > cost:
                best_list.append({"move": None, "route": route, "cost": cost, "n_vehicles": n_vehicles})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: (x["n_vehicles"], x["cost"]))    

    return sorto[0]

def swap_3_3(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(3+i, len(best["route"])-2):
            route = best["route"][:]
            swap = route[i:i+3]
            route[i:i+3]=  route[j:j+3]
            route[j:j+3] = swap

            cost = calculate_route_cost(cost_function, route)
            n_vehicles = count_vehicle(route, q, Q)

            if best["n_vehicles"] > n_vehicles and best["cost"] > cost:
                        best_list.append({"move": None, "route": route, "cost": cost, "n_vehicles": n_vehicles})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: (x["n_vehicles"], x["cost"]))    

    return sorto[0]

def last_go_first(best, cost_function, q, Q):
    route = best["route"][:]

    first = route[len(route)-1]
    del route[len(route) - 1]
    route[1:len(route)-1] = route[0:len(route)-1]
    route[0] = first

    cost = calculate_route_cost(cost_function, route)
    n_vehicles = count_vehicle(route, q, Q)

    if cost < best["cost"]:
        return {"move": None, "route": route, "cost": cost}
    
    return best

def swap_2_1(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(2+i, len(best["route"])-1):
            route = best["route"][:]
            swap = route[i:i+2]
            singleton = route[j]
            del route[j]
            route[i] = singleton
            route[i+1:i+2] = swap

            cost = calculate_route_cost(cost_function, route)
            n_vehicles = count_vehicle(route, q, Q)

            if best["n_vehicles"] > n_vehicles and best["cost"] > cost:
                        best_list.append({"move": None, "route": route, "cost": cost, "n_vehicles": n_vehicles})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: (x["n_vehicles"], x["cost"]))    

    return sorto[0]