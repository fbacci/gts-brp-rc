from docplex.mp.model import Model
from copy import deepcopy

def get_reduced_cost_index(source, target, reduced_costs):
    i = 0
    reduced_costs_index = []
    for (s, _) in source:
        for (t, _) in target:
            reduced_costs_index.append(((s,t), reduced_costs[i]))
            i += 1
    
    return reduced_costs_index

def generate_artificial_node(total_demand, total_supply, target, source, c_copy, n):
    if abs(total_demand) > total_supply:
        source.append((n, abs(total_demand) - total_supply))
        for (t, q) in target:
            c_copy[(n, t)] = 0
    else:
        target.append((n, -(total_supply - abs(total_demand))))
        for(s, q) in source:
            c_copy[(s, n)] = 0

    print(total_supply, total_demand)
    print(source, target)

    return target, source

def build_target_source(N, n, q, c_copy):
    target = []
    source = []
    total_demand = 0
    total_supply = 0

    for node in N:
        if q[node] < 0:
            total_demand += q[node]
            target.append((node, q[node]))
        else:
            total_supply += q[node]
            source.append((node, q[node]))

    #generate artificial nodes
    target, source = generate_artificial_node(total_demand, total_supply, target, source, c_copy, n)
    
    return target, source, total_demand, total_supply

def solve_transportation_problem(N, n, c, q):
    model = Model(name='transshipment')
    A = []
    c_copy = deepcopy(c)

    #split nodes in supply (source) and deficit(target)
    target, source, total_demand, total_supply = build_target_source(N, n, q, c_copy)

    for (t, _) in target:
        for(s, _) in source:
            A.append((s, t))

    # initialize decision variable
    x = {(s,t): model.continuous_var(name='x_{0}_{1}'.format(s,t)) for (s, _) in source for (t, _) in target}

    # variable to check if target has already been visited, so it must receive the total individual demand
    b = {t: model.continuous_var(name='b_{0}'.format(t)) for (t, _) in target}

    # define objective function
    model.minimize(model.sum(x[s,t]*c_copy.get((s,t), 0) for (s, _) in source for (t, _) in target))

    # set constraints
    # for each source node, total outgoing flow must be smaller than available quantity
    for (s, q) in source:
        model.add_constraint(model.sum(x[s,t] for (t, _) in target) <= q)
        
    # for each target node, total ingoing flow must be greater than demand
    for (t, q) in target:
        model.add_constraint(model.sum(x[s,t] for (s, _) in source) >= abs(q))

    # constraint on b, not working (non funziona perché da nessuna parte la incrementiamo, semplicemente le setta a 1, forse deve basarsi su x?)
    model.add_constraints(b[t] == 1 for (t, _) in target)

    solution = model.solve()
    reduced_costs = model.reduced_costs(x[s,t] for (s, _) in source for (t, _) in target)
    reduced_costs = get_reduced_cost_index(source, target, reduced_costs)

    return solution, reduced_costs
