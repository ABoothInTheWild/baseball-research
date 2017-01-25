# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 18:46:58 2017

@author: Alexander
"""

from scipy.optimize import linprog
import numpy as np

#Callback as defined from 
#https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linprog.html
def linprog_callback(xk, **kwargs):

    tableau = kwargs["tableau"]
    nit = kwargs["nit"]
    pivrow, pivcol = kwargs["pivot"]
    phase = kwargs["phase"]
    basis = kwargs["basis"]

    saved_printoptions = np.get_printoptions()
    np.set_printoptions(linewidth=500,
                        formatter={'float':lambda x: "{: 12.4f}".format(x)})
                        
    print("--------- Iteration {:d}  - Phase {:d} --------\n".format(nit, phase))
    print("Tableau:")

    if iter >= 0:
        print("" + str(tableau) + "\n")
        print("Pivot Element: T[{:.0f}, {:.0f}]\n".format(pivrow, pivcol))
        print("Basic Variables:", basis)
        print()
        print("Current Solution:")
        print("x = ", xk)
        print()
        print("Current Objective Value:")
        print("f = ", -tableau[-1, -1])
        print()
    np.set_printoptions(**saved_printoptions)
    
#No limits 
#minimze equation
c = [1, 1, 1, 1]
 
A = [[-1, -1, -1, -1],
      [-1, -2, -3, -4]]

#Coefficients. Negative to represent upper bound
B = [-209.4, -372.6]

x_bounds = (0, None)
y_bounds = (0, None)
z_bounds = (0, None)
w_bounds = (48, None)

bounds = (x_bounds, y_bounds, z_bounds, w_bounds)

res = linprog(c, A_ub=A, b_ub=B, bounds=bounds, callback = linprog_callback, options={"disp": True})

print(res)

#Limit HRs
#minimize equation
c = [1, 1, 1, 1]

#Coefficients. Negative to represent upper bound
A = [[-1, -1, -1, -1],
      [-1, -2, -3, -4]]

B = [-209.4, -372.6]

x_bounds = (0, None)
y_bounds = (0, None)
z_bounds = (0, None)
w_bounds = (48, 48)

bounds = (x_bounds, y_bounds, z_bounds, w_bounds)

res = linprog(c, A_ub=A, b_ub=B, bounds=bounds, callback = linprog_callback, options={"disp": True})

print(res)

#Limit triples and SLG
#minimize equation
c = [1, 1, 1, 1]
 
#Coefficients. Negative to represent upper bound
A = [[-1, -1, -1, -1],
      [-1, -2, -3, -4],
      [1, 2, 3, 4]]

B = [-209.4, -372.6, 390]

x_bounds = (0, None)
y_bounds = (0, None)
z_bounds = (0, 1)
w_bounds = (48, 48)

bounds = (x_bounds, y_bounds, z_bounds, w_bounds)

res = linprog(c, A_ub=A, b_ub=B, bounds=bounds, callback = linprog_callback, options={"disp": True})

print(res)