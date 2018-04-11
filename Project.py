
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
model.R = Var(model.Time, model.Activity, within=NonNegativeReals)# hours worked by regular employees
model.P = Var(model.Time, model.Activity, within=NonNegativeReals)# hours worked by prestige

#Objective Function 
def objective_rule(model):
    return sum (model.RCost[i] * model.R[i,j] + model.PCost[i] * model.P[i,j] for i in model.Type for j in model.Activity)
model.TotalCost = Objective (rule=objective_rule, sense=minimize)
#Minimizing the total cost of regular and prestige workers

#declaring the constraints
def FTRegHr_rule(model):
    return 40 <= model.R[i,j] <= 60
model.RegularFTHours = Constraint (rule=FTRegHr_rule) #Full time regular workers must work between 40 and 60 hrs a week

def FTPreHr_rule(model):
    return 40 <= model.P[i,j] <= 60
model.PrestigeFTHours = Constraint (rule=FTPreHr_rule)  #Full time prestige workers must work between 40 and 60 hrs a week
