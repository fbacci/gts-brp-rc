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

def build_target_source(N, n, q):
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

    #set demand deposit
    if abs(total_demand) > total_supply:
        q[0] = abs(total_demand) - total_supply
        source.append((0, q[0]))
    else:
        q[0] = -(total_supply - abs(total_demand))
        target.append((0, q[0]))
    
    return target, source

def solve_transportation_problem(N, n, c, q):
    model = Model(name='transshipment')
    A = []

    #split nodes in supply (source) and deficit(target)
    target, source = build_target_source(N, n, q)

    for (t, _) in target:
        for(s, _) in source:
            A.append((s, t))

    # initialize decision variable
    x = {(s,t): model.continuous_var(name='x_{0}_{1}'.format(s, t)) for (s, _) in source for (t, _) in target}

    # define objective function
    model.minimize(model.sum(x[s, t] * c.get((s, t), 0) for (s, _) in source for (t, _) in target))

    # set constraints
    # for each source node, total outgoing flow must be smaller than available quantity
    for (s, q) in source:
        model.add_constraint(model.sum(x[s, t] for (t, _) in target) <= q)
        
    # for each target node, total ingoing flow must be greater than demand
    for (t, q) in target:
        model.add_constraint(model.sum(x[s, t] for (s, _) in source) >= abs(q))

    solution = model.solve()
    reduced_costs = model.reduced_costs(x[s, t] for (s, _) in source for (t, _) in target)
    reduced_costs = get_reduced_cost_index(source, target, reduced_costs)

    return solution, reduced_costs
