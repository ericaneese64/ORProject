
#Caleb Wheelock
#Project Problem

from pyomo.environ import *

#create model object
model=AbstractModel()

#Sets
model.Shift = Set()#1=8-10, 2=10-12, 3=12-2, 4=2-4, 5=4-6, 6=6-8, 7=8-10
model.Time = Set()# FT=Full Time PT=Part Time OT=Over Time

#Parameters


#Declaring decision variables:
model.R= Var(model.Shift, model.Time, within=NonNegativeReals)# number of regular employees for each 2hr block of the workday
model.P= Var(model.Shift, model.Time, within=NonNegativeReals)# number of prestige employees for each 2hr block of the workday
model.S= Var(model.Shift, model.Time, within=NonNegativeReals)# number of student employees for each 2hr block of the workday

#Objective Function 
def objective_rule(model):
    return sum (model.R[i,j] + model.P[i,j] + model.S[i,j] for i in model.Shift for j in model.Time)
model.TotalWorkers = Objective (rule=objective_rule, sense=minimize)
#Minimizing the total number of regular and prestige workers needed for a day of work

'*********************************************************Declaring the Constraints******************************************************'
#Shift Constraints
def Shift1_rule(model,i,j):
    return model.R['1',j] + model.P['1',j] >= 4
model.Shift1Constraint = Constraint(model.Shift, model.Time, rule=Shift1_rule)
#Shift 1 Constraint: 8-10 Adult Open Gym req 4 workers

def Shift2_rule(model,i,j):
    return model.R['1',j] + model.P['1',j] + model.R['2',j] + model.P['2',j] >= 3
model.Shift2Constraint = Constraint(model.Shift, model.Time, rule=Shift2_rule)
#Shift 2 Constraint: 10-12 Class req 6 workers

def Shift3_rule(model,i,j):
    return model.R['1',j] + model.P['1',j] + model.R['2',j] + model.P['2',j] + model.R['3',j] + model.P['3',j] >= 6
model.Shift3Constraint = Constraint(model.Shift, model.Time, rule=Shift3_rule)
#Shift 3 Constraint: 12-2 Open Gym/Birthday Time req 6 workers

def Shift4_rule(model,i,j):
    return model.R['1',j] + model.P['1',j] + model.R['2',j] + model.P['2',j] + model.R['3',j] + model.P['3',j] + model.R['4',j] + model.P['4',j] >= 6
model.Shift4Constraint = Constraint(model.Shift, model.Time, rule=Shift4_rule)
#Shift 4 Constraint: 2-4 Open Gym/Birthday Time req 6 workers

def Shift5_rule(model,i,j):
    return model.R['2',j] + model.P['2',j] + model.R['3',j] + model.P['3',j] + model.R['4',j] + model.P['4',j] + model.R['5',j] + model.P['5',j] + model.S['5',j] >= 6
model.Shift5Constraint = Constraint(model.Shift, model.Time, rule=Shift5_rule)
#Shift 5 Constraint: 4-6 Family Open Gym req 6 workers

def Shift6_rule(model,i,j):
    return model.R['3',j] + model.P['3',j] + model.R['4',j] + model.P['4',j] + model.R['5',j] + model.P['5',j] + model.S['5',j] + model.R['6',j] + model.P['6',j] + model.S['6',j] >= 6
model.Shift6Constraint = Constraint(model.Shift, model.Time, rule=Shift6_rule)
#Shift 6 Constraint: 6-8 Family Open Gym req 6 workers

def Shift7_rule(model,i,j):
    return model.R['4',j] + model.P['4',j] + model.R['5',j] + model.P['5',j] + model.S['5',j] + model.R['6',j] + model.P['6',j] + model.S['6',j] + model.R['7',j] + model.P['7',j] + model.S['7',j] >= 4
model.Shift7Constraint = Constraint(model.Shift, model.Time, rule=Shift7_rule)
#Shift 7 Constraint: 8-10 Adult Open Gym Time req 6 workers

def BDay3_rule(model,i,j):
    return model.P['2',j] + model.P['3',j] >= 1
model.BDay3Constraint = Constraint(model.Shift, model.Time, rule=BDay3_rule)
#Birthday needs at least one prestige worker for shift 3

def BDay4_rule(model,i,j):
    return model.P['3',j] + model.P['4',j] >= 1
model.BDay4Constraint = Constraint(model.Shift, model.Time, rule=BDay4_rule)
#Birthday needs at least one prestige workerfor shift 4



#def OTRegHr_rule(model,i,j):
#    return 45 <= model.R[i,'OT'] <= 60
#model.RegularOTHours = Constraint (model.Shift, model.Time, rule=OTRegHr_rule) #OT regular workers must work between 40 and 60 hrs a week
#
#def OTPreHr_rule(model,i,j):
#    return 45 <= model.P[i,'OT'] <= 60
#model.PrestigeOTHours = Constraint (model.Shift, model.Time, rule=OTPreHr_rule)  #OT prestige workers must work between 40 and 60 hrs a week
#
#def FTRegHr_rule(model,i,j):
#    return 40 <= model.R[i,'FT'] <= 44
#model.RegularFTHours = Constraint (model.Shift, model.Time, rule=FTRegHr_rule) #Full time regular workers must work 40 hrs a week
#
#def FTPreHr_rule(model,i,j):
#    return 40 <= model.P[i,'FT'] <= 44
#model.PrestigeFTHours = Constraint (model.Shift, model.Time, rule=FTPreHr_rule) #Full time prestige workers must work 40 hrs a week
#
#def PTRegHr_rule(model,i,j):
#    return 20 <= model.R['PT',j] <= 29.5
#model.RegularPTHours = Constraint (model.Shift, model.Time, rule=PTRegHr_rule) #Part time regular workers must work between 20 and 29.5 hrs a week
#
#def PTPreHr_rule(model,i,j):
#    return 20 <= model.P['PT',j] <= 29.5
#model.PrestigePTHours = Constraint (model.Shift, model.Time, rule=PTPreHr_rule)  #Part time prestige workers must work between 20 and 29.5 hrs a week
#
#def PTStuHr_rule(model,i,j):
#    return 20 <= model.S['PT',j] <= 29.5
#model.StudentPTHours = Constraint (model.Shift, model.Time, rule=PTPreHr_rule)  #Part time student workers must work between 20 and 29.5 hrs a week

#Step 1: Load the Model
data = DataPortal()
data.load(filename="ProjectData.dat")

#Step 2: Create a SolverFactory and Model Instance
optimizer = SolverFactory('glpk')
instance = model.create_instance(data)

#Step 3: Run the Model and display Results
optimizer.solve(instance)
instance.display()