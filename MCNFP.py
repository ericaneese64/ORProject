#MCNFP
from pyomo.environ import*

model=AbstractModel()

model.NODES = Set()
model.ARCS = Set(within = model.NODES*model.NODES)

model.netDemand = Param(model.NODES)
model.cost = Param(model.ARCS)

#Decision Variables
model.x = Var(model.ARCS, within=NonNegativeReals)

def objective_rule(model):
	return sum(model.cost[i,j]*model.x[i,j] for (i,j) in model.ARCS)
	
model.totalCost = Objective(rule=objective_rule, sense=minimize)

#net demand constraints
def net_demand_rule(model,i):
	return(sum(model.x[k,i] for k in model.NODES if (k,i) in model.ARCS) \
	-sum(model.x[i,j] for j in model.NODES if (i,j) in model.ARCS) \
	== model.netDemand[i])
	
model.netDemandConstraints = Constraint (model.NODES, rule=net_demand_rule)