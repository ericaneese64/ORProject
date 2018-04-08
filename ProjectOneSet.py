# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 08:16:25 2018

@author: cpw1064
"""
#Caleb Wheelock
#Police problem

from pyomo.environ import *

#create model object
model=AbstractModel()

#Sets
model.Type = Set()# type of worker part time (PT), full time (FT), part time prestige (PTP), full time prestige (FTP), overtime full time (OTF), overtime prestige (OTP)

model.Activity = Set()# activity: adult gym (AG), family gym (FG), class (C), birthday party (BP)

#Parameters
model.Cost = Param(model.Type)

#declaring decision variables:
model.x = Var(model.Type, model.Activity, within=NonNegativeReals)#  how many of each type of ninja

#Objective Function 
def objective_rule(model):
    return sum (model.Cost[j] * model.x[i,j] for i in model.Type for j in model.Activity)
model.TotalCost = Objective (rule=objective_rule, sense=minimize)

#declaring the constraints
def FT_rule(model,i):
    return 40 <= 
model.available_oranges = Constraint(model.Quality, rule=oranges_rule)
