from utils import calculate_route_cost as crc
from SplitRoute import convert_tsp_to_vrp
from itertools import accumulate

def calculate_route_cost(cost_function, route, q, Q):
    vrp_route = convert_tsp_to_vrp(route, q, len(route), Q, cost_function)
    vrp_route = list(filter(None, vrp_route))


    sum_qp = list(accumulate([q[node] for node in route]))
    qp_max = max([0, max(sum_qp)])
    qp_min = min(sum_qp)

    if qp_min > 0:
        qp_min = 0

    vrp_cost = 0
    for trip in vrp_route:
        vrp_cost += crc(cost_function, trip)

    costo = crc(cost_function, route)


    costo2 =  costo + (qp_max + abs(qp_min))*(costo/abs(sum([abs(c) for c in q])))

    return vrp_cost, costo, costo2, qp_min, qp_max


def move(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(0, len(best["route"])):
            route = best["route"][:]
            del route[i]
            route.insert(j, best["route"][i])

            cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

            if cost < best["cost"]:
                best_list.append({"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: x["cost"])  
    mino = min(best_list, key = lambda x: x["costo2"])   

    mino2 = min(best_list, key = lambda x: x["costo"])
    #print(sorto.index(mino2), sorto.index(mino))
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

            cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

            if cost < best["cost"]:
                best_list.append({"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: x["cost"])  
    mino = min(best_list, key = lambda x: x["costo2"])   

    mino2 = min(best_list, key = lambda x: x["costo"])
    #print(sorto.index(mino2), sorto.index(mino))
    return sorto[0]

def swap_1_1(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(i+1, len(best["route"])):
            route = best["route"][:]
            route[i], route[j] = route[j], route[i]

            cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

            if cost < best["cost"]:
                best_list.append({"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: x["cost"])  
    mino = min(best_list, key = lambda x: x["costo2"])   

    mino2 = min(best_list, key = lambda x: x["costo"])
    #print(sorto.index(mino2), sorto.index(mino))
    return sorto[0]

def swap_2_2(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(2+i, len(best["route"])-1):
            route = best["route"][:]
            swap = route[i:i+2]
            route[i:i+2]=  route[j:j+2]
            route[j:j+2] = swap

            cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

            if cost < best["cost"]:
                best_list.append({"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: x["cost"])  
    mino = min(best_list, key = lambda x: x["costo2"])   

    mino2 = min(best_list, key = lambda x: x["costo"])
    #print(sorto.index(mino2), sorto.index(mino))
    return sorto[0]

def swap_1_1_1(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(i+1, len(best["route"])):
            for k in range(j+1, len(best["route"])):
                route = best["route"][:]

                route[i], route[j], route[k] = route[j], route[k], route[i]

                cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

                if cost < best["cost"]:
                    best_list.append({"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax})
                
                route[i], route[j], route[k] = route[k], route[i], route[j]

                cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

                if cost < best["cost"]:
                    best_list.append({"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax})          

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: x["cost"])  
    mino = min(best_list, key = lambda x: x["costo2"])   

    mino2 = min(best_list, key = lambda x: x["costo"])
    #print(sorto.index(mino2), sorto.index(mino))
    return sorto[0]

def swap_3_3_reversed(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(3+i, len(best["route"])-2):
            route = best["route"][:]
            swap = route[i:i+3]
            route[i:i+3]=  route[j:j+3]
            route[j:j+3] = reversed(swap)

            cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

            if cost < best["cost"]:
                best_list.append({"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: x["cost"])  
    mino = min(best_list, key = lambda x: x["costo2"])   

    mino2 = min(best_list, key = lambda x: x["costo"])
    #print(sorto.index(mino2), sorto.index(mino))
    return sorto[0]

def swap_3_3(best, cost_function, q, Q):
    best_list = []

    for i in range(0, len(best["route"])):
        for j in range(3+i, len(best["route"])-2):
            route = best["route"][:]
            swap = route[i:i+3]
            route[i:i+3]=  route[j:j+3]
            route[j:j+3] = swap

            cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

            if cost < best["cost"]:
                best_list.append({"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: x["cost"])  
    mino = min(best_list, key = lambda x: x["costo2"])   

    mino2 = min(best_list, key = lambda x: x["costo"])
    #print(sorto.index(mino2), sorto.index(mino))
    return sorto[0]

def last_go_first(best, cost_function, q, Q):
    route = best["route"][:]

    first = route[len(route)-1]
    del route[len(route) - 1]
    route[1:len(route)-1] = route[0:len(route)-1]
    route[0] = first

    cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

    if cost < best["cost"]:
        return {"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax}
    
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

            cost, costo,costo2,qpmin,qpmax= calculate_route_cost(cost_function, route, q, Q)

            if cost < best["cost"]:
                best_list.append({"move": None, "route": route, "cost": cost, "costo": costo, "costo2": costo2,"qpmin": qpmin, "qpmax": qpmax})

    if len(best_list) == 0:
        return best
    
    sorto = sorted(best_list, key = lambda x: x["cost"])  
    mino = min(best_list, key = lambda x: x["costo2"])   

    mino2 = min(best_list, key = lambda x: x["costo"])
    #print(sorto.index(mino2), sorto.index(mino))
    return sorto[0]