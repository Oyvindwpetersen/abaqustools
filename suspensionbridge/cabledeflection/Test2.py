# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 12:38:58 2022

@author: oyvinpet
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:35:26 2022

@author: oyvinpet
"""

import numpy as np
import scipy
import line_profiler
import cProfile

#%%

@profile
def pythagoras(a,b):

    c=a**2+b**2
    
    return c