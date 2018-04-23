#Caleb Wheelock

from pyomo.environ import*
#Declare Model
model=AbstractModel()

#sets
model.SUPPLIES = Set() #supply nodes
model.DEMANDS = Set() #demand nodes

#parameters
model.s = Param(model.SUPPLIES) #supply avail at each node
model.d = Param(model.DEMANDS) #demand req at each node
model.c = Param(model.SUPPLIES, model.DEMANDS) #shipping cost from supply point i to demand point j
#model.p = Param(model.SUPPLIES)

#decision variables: x[ij] = amount shipped from supply point i to demand point j
model.x = Var(model.SUPPLIES, model.DEMANDS, within = NonNegativeReals)

#objective function: min cost to meet demands
def objective_rule(model):
    return sum(model.c[i,j] * model.x[i,j] for i in model.SUPPLIES for j in model.DEMANDS)
model.minCost = Objective(rule=objective_rule, sense=minimize)

#Supply Constraint
def supply_rule(model,i):
    return (sum(model.x[i,j] for j in model.DEMANDS) == model.s[i] )
model.supplyConstraints = Constraint(model.SUPPLIES, rule=supply_rule)

#Demand Constraint
def demand_rule(model,j):
    return (sum(model.x[i,j] for i in model.SUPPLIES) == model.d[j])
model.demandConstraints = Constraint(model.DEMANDS, rule=demand_rule)

'**********************************************Running the Model****************************************'
data = DataPortal()
data.load(filename="ProjectDataFinal.dat", model=model)

optimizer = SolverFactory("glpk")
instance = model.create_instance(data)

optimizer.solve(instance)
instance.display()
