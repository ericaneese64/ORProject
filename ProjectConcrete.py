
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
#Minimizing the total cost of regular and prestige workers

'*********************************************************Declaring the Constraints******************************************************'
#Shift Constraints
def FTRegHr_rule(model,i,j):
    return 40 <= model.R['FT',j] <= 60
model.RegularFTHours = Constraint (model.Time, model.Activity, rule=FTRegHr_rule) #Full time regular workers must work between 40 and 60 hrs a week

def FTPreHr_rule(model,i,j):
    return 40 <= model.P['FT',j] <= 60
model.PrestigeFTHours = Constraint (model.Time, model.Activity, rule=FTPreHr_rule)  #Full time prestige workers must work between 40 and 60 hrs a week

def PTRegHr_rule(model,i,j):
    return 20 <= model.R['PT',j] <= 29.5
model.RegularPTHours = Constraint (model.Time, model.Activity, rule=PTRegHr_rule) #Part time regular workers must work no more than 29.5 hrs a week

def PTPreHr_rule(model,i,j):
    return 20 <= model.P['PT',j] <= 29.5
model.PrestigePTHours = Constraint (model.Time, model.Activity, rule=PTPreHr_rule)  #Part time prestige workers must work no more than 29.5 hrs a week

#Scheduling Constraints
def AG_rule(model,i,j):
    return model.R[i,'AG'] + model.P[i,'AG'] >= 96
model.AGReq = Constraint (model.Time, model.Activity, rule=AG_rule) #Adult Gym needs at least 4 workers (4 workers * 24 hrs AG per week = 96 hrs/wk)

def FG_rule(model,i,j):
    return model.R[i,'FG'] + model.P[i,'FG'] >= 144
model.FGReq = Constraint (model.Time, model.Activity, rule=FG_rule) #Family Gym needs at least 6 workers (6 workers * 24 hrs FG per week = 144 hrs/wk)

def C_rule(model,i,j):
    return model.R[i,'C'] + model.P[i,'C'] >= 30
model.CReq = Constraint (model.Time, model.Activity, rule=C_rule) #Class needs at least 3 workers (3 workers * 10 hrs C per week = 30 hrs/wk)

def BP_rule(model,i,j):
    return model.R[i,'BP'] + model.P[i,'BP'] >= 54
model.BPReq = Constraint (model.Time, model.Activity, rule=BP_rule) #Birthday Party needs at least 6 workers (6 workers * 9 hrs BP per week = 54 hrs/wk)

def BPPre_rule(model,i,j):
    return model.P[i,'BP'] >= 9
model.BPPreReq = Constraint (model.Time, model.Activity, rule=BP_rule) #Birthday Party needs at least 1 prestige workers (1 prestige worker * 9 hrs AG per week = 54 hrs/wk)



