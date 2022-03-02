# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 12:42:37 2022

@author: oyvinpet
"""


#%%


from line_profiler import LineProfiler
import random



def do_stuff2(numbers):
    ss = sum(numbers)+sum(numbers)
    
def do_stuff(numbers):
    s = sum(numbers)
    l = [numbers[i]/43 for i in range(len(numbers))]
    m = ['hello'+str(numbers[i]) for i in range(len(numbers))]
    
    n=do_stuff2(numbers)
    

    
    
    
numbers = [np.random.randn(1,100) for i in range(1000)]

lp = LineProfiler()
lp_wrapper = lp(do_stuff)
lp_wrapper(numbers)
lp.print_stats()

#%%

from Assembly import Assembly

lp = LineProfiler()
lp_wrapper = lp(Assembly)
lp_wrapper(r,RT,ModelInfo)
lp.print_stats()


#%%

from Corot import K_el_matrix
from Corot import K_el_matrix

lp = LineProfiler()
lp_wrapper = lp(K_el_matrix_test)
lp_wrapper(r_sub,RT_sub,A,Iz,Iy,It,E,G,X1,X2,e2,TC0)
lp.print_stats()




    A = A.toarray()
    N = np.shape(A)[0]
    D = np.count_nonzero(A[0,:])
    ab = np.zeros((D,N))
    for i in np.arange(1,D):
        ab[i,:] = np.concatenate((np.diag(A,k=i),np.zeros(i,)),axis=None)
    ab[0,:] = np.diag(A,k=0)
    y = solveh_banded(ab,x,lower=True)
