# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 13:55:50 2017

@author: t2adb
"""

from itertools import combinations

#Chipotle Combinations

#Alexander Booth
#April 11, 2017

def chipotleCombinations(containers, meat, rice, beans, toppings):
    
    #combinations of choosing any and all meats
    meat_combine= 0
    for meatNum in range(meat + 1):
        meat_combine += len(list(combinations(range(meat), meatNum)))
    
    #combinations of choosing any and all rice
    rice_combine = 0
    for riceNum in range(rice + 1):
        rice_combine += len(list(combinations(range(rice), riceNum)))
    
    #combinations of choosing any and all beans
    bean_combine = 0
    for beanNum in range(beans + 1):
        bean_combine += len(list(combinations(range(beans), beanNum)))
        
    #combinations of choosing any and all toppings
    toppings_combine = 0
    for toppNum in range(toppings + 1):
        toppings_combine += len(list(combinations(range(toppings), toppNum)))
      
    #calculate total combinations
    total_comb = containers * meat_combine * rice_combine * bean_combine * toppings_combine
    
    return(total_comb)

#Check Against Hendricks:
#Burrito or Bowl or 2 types of tacos or salad
containers_old = 5
#Meat/Filling
#chicken, steak, barbacoa, carnitas
meat_old = 4
#Rice
#white, brown
rice_old = 2
#Beans
#pinto, black
beans_old = 2
#Toppings
#guac, tomatoes, corn, mild salsa, spicy salsa, 
#sour cream, veggies, lettuce, cheese
toppings_old = 9

total_chipotle_old = chipotleCombinations(containers_old, meat_old, rice_old, beans_old, toppings_old)
print("The total combinations of Chipotle with those inputs are: %d" %total_chipotle_old)
#The total combinations of Chipotle with those inputs are: 655360
#It matches!

#Current Possibilities
#Burrito or Bowl or 3 types of tacos or salad
containers = 6
#Meat/Filling
#chicken, steak, barbacoa, carnitas, chorizo, sofritas, veggies
meat = 7
#Rice
#white, brown
rice = 2
#Beans
#pinto, black
beans = 2
#Toppings
#guac, tomatoes, corn, mild salsa, spicy salsa, 
#sour cream, veggies, lettuce, cheese
toppings = 9

total_chipotle = chipotleCombinations(containers, meat, rice, beans, toppings)
print("The total combinations of Chipotle with those inputs are: %d" %total_chipotle)
#The total combinations of Chipotle with those inputs are: 1048576