#Caleb Wheelock, Jacob Smythe, Michael Halligan, Erica Neese

from pyomo.environ import*
#Declare Model
model=AbstractModel()

#sets
model.SUPPLIES = Set() #supply nodes: Each worker
model.DEMANDS = Set() #demand nodes: Each shift for part and full time workers

#parameters
model.s = Param(model.SUPPLIES) #supply of hours available for each worker
model.d = Param(model.DEMANDS) #demand required for each shift
model.c = Param(model.SUPPLIES, model.DEMANDS) #wage per hour for each worker for a given shift

#decision variables: x[ij] = amount of hours each worker i works for shift j
model.x = Var(model.SUPPLIES, model.DEMANDS, within = NonNegativeReals)

#objective function: minimize the daily cost of labor for each worker i and shift j
def objective_rule(model):
    return sum(model.c[i,j] * model.x[i,j] for i in model.SUPPLIES for j in model.DEMANDS)
model.minCost = Objective(rule=objective_rule, sense=minimize)

#Supply Constraint: The total 
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
