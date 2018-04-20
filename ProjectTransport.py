#Caleb Wheelock

from pyomo.environ import*
#Declare Model
model=AbstractModel()

#sets
model.SUPPLIES = Set() #supply nodes
model.DEMANDS = Set() #demand nodes
model.FulltimeSUPPLIES = Set() #full time supply nodes
model.PrestigeSUPPLIES = Set() #prestige supply nodes

#parameters
model.s = Param(model.SUPPLIES) #supply avail at each node
model.d = Param(model.DEMANDS) #demand req at each node
model.c = Param(model.SUPPLIES, model.DEMANDS) #shipping cost from supply point i to demand point j

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

##Full Time 8 Hour Block
#def FullTime1_rule(model,i):
#    return model.x[i,'FG'] + model.x[i,'BP'] >= 56
#model.FTReq1 = Constraint(model.FulltimeSUPPLIES, rule=FullTime1_rule)
#
#def FullTime2_rule(model,i):
#    return model.x[i,'BP'] + model.x[i,'CL'] >= 56
#model.FTReq2 = Constraint(model.FulltimeSUPPLIES, rule=FullTime2_rule)
#
#def FullTime3_rule(model,i):
#    return model.x[i,'CL'] + model.x[i,'AG'] >= 56
#model.FTReq3 = Constraint(model.FulltimeSUPPLIES, rule=FullTime3_rule)
#
##Full Time 8 Hour Block
##def FullTime_rule(model,i):
##    if model.t[i] == 'FT':
##        return model.x[i,j] + model.x[i,j+1] == 2
##    else:
##        pass
##model.FTReq = Constraint(model.SUPPLIES, rule=FullTime_rule)
#
##Birthday Requirement
#def BDay_rule(model):
#    return sum(model.x[i,'BP'] for i in model.PrestigeSUPPLIES) >= 28
#model.BDayReq = Constraint(rule=BDay_rule)

'**********************************************Running the Model****************************************'
data = DataPortal()
data.load(filename="ProjectData3.dat", model=model)

optimizer = SolverFactory("glpk")
instance = model.create_instance(data)

optimizer.solve(instance)
instance.display()
