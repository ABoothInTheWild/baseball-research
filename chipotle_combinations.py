# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 13:55:50 2017

@author: t2adb
"""

from itertools import combinations

#Chipotle Combinations

#Alexander Booth
#February 3, 2017

def chipotleCombinations(containers, fillings, rice, beans, toppings):
    
    #combinations of choosing any and all meats
    meat_combine= 0
    for meatNum in range(fillings + 1):
        meat_combine += len(list(combinations(range(fillings), meatNum)))
    
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

#Current Possibilities

#Burrito or Bowl or 3 types of tacos or salad
#But we'll just stick to a burrito
containers = 1
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