
#Caleb Wheelock
#Project Problem

from pyomo.environ import *

#create model object
model=AbstractModel()

#Sets
model.Time = Set()# regular time, overtime, or part time worked
model.Activity = Set()# activity: adult gym (AG), family gym (FG), class (C), birthday party (BP)

#Parameters
model.RCost = Param(model.Time)# Regular cost of worker
model.PCost = Param(model.Time)# Prestige cost of worker
model.WeeklyHrs = Param(model.Activity)

#Declaring decision variables:
model.R = Var(model.Time, model.Activity, within=NonNegativeReals)# hours worked by a regular employee in a week
model.P = Var(model.Time, model.Activity, within=NonNegativeReals)# hours worked by a prestige employee in a week

#Objective Function 
def objective_rule(model):
    return sum (model.RCost[i] * model.R[i,j] + model.PCost[i] * model.P[i,j] for i in model.Time for j in model.Activity)
model.TotalCost = Objective (rule=objective_rule, sense=minimize)
#Minimizing the total cost of regular and prestige workers for a week

'*********************************************************Declaring the Constraints******************************************************'
#Shift Constraints
def OTRegHr_rule(model,i,j):
    return 40 <= model.R['OT',j] <= 60
model.RegularOTHours = Constraint (model.Time, model.Activity, rule=OTRegHr_rule) #OT regular workers must work between 40 and 60 hrs a week

def OTPreHr_rule(model,i,j):
    return 40 <= model.P['OT',j] <= 60
model.PrestigeOTHours = Constraint (model.Time, model.Activity, rule=OTPreHr_rule)  #OT prestige workers must work between 40 and 60 hrs a week

def FTRegHr_rule(model,i,j):
    return model.R['FT',j] == 40
model.RegularFTHours = Constraint (model.Time, model.Activity, rule=FTRegHr_rule) #Full time regular workers must work 40 hrs a week

def FTPreHr_rule(model,i,j):
    return model.P['FT',j] == 40
model.PrestigeFTHours = Constraint (model.Time, model.Activity, rule=FTPreHr_rule) #Full time prestige workers must work 40 hrs a week

def PTRegHr_rule(model,i,j):
    return 20 <= model.R['PT',j] <= 29.5
model.RegularPTHours = Constraint (model.Time, model.Activity, rule=PTRegHr_rule) #Part time regular workers must work between 20 and 29.5 hrs a week

def PTPreHr_rule(model,i,j):
    return 20 <= model.P['PT',j] <= 29.5
model.PrestigePTHours = Constraint (model.Time, model.Activity, rule=PTPreHr_rule)  #Part time prestige workers must work between 20 and 29.5 hrs a week

#Scheduling Constraints
def Active_rule(model,i,j):
    return model.R[i,j] + model.P[i,j] >= model.WeeklyHrs[j]
model.ActiveReq = Constraint (model.Time, model.Activity, rule=Active_rule) #Activity j needs enough workers to account for the demand of that activity each week

def BP_rule(model,i,j):
    return model.P[i,'BP'] >= 9
model.BPReq = Constraint (model.Time, model.Activity, rule=BP_rule) #Birthday Party needs at least 1 prestige workers (1 prestige worker * 9 hrs AG per week = 54 hrs/wk)

