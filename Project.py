
#Caleb Wheelock
#Project Problem

from pyomo.environ import *

#create model object
model=AbstractModel()

#Sets
model.Time = Set()# regular time overtime or part time worked
model.Activity = Set()# activity: adult gym (AG), family gym (FG), class (C), birthday party (BP)

#Parameters
model.RCost = Param(model.Time)# Regular cost of worker
model.PCost = Param(model.Time)# Prestige cost of worker

#Declaring decision variables:
model.R = Var(model.Type, model.Activity, within=NonNegativeReals)# hours worked by regular employees
model.P = Var(model.Type, model.Activity, within=NonNegativeReals)# hours worked by prestige

#Objective Function 
def objective_rule(model):
    return sum (model.RCost[i] * model.R[i,j] + model.PCost[i] * model.P[i,j] for i in model.Type for j in model.Activity)
model.TotalCost = Objective (rule=objective_rule, sense=minimize)

#declaring the constraints
def FT_rule(model):
    return 40 <= model.F[i,j] + model.O[i,j] <= 60