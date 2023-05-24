# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:36:35 2022

@author: oyvinpet
"""

#%%

import sys

sys.path.append('C:/Cloud/OD_OWP/Work/Python/Github')

# import abaqustools
from abaqustools import odbexport

#%%

folder_odb='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/odbexport_example'
jobname='Model_single_deck'
folder_save=folder_odb
folder_python='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport'

odbexport.export.modal(folder_odb,jobname,folder_save,folder_python)


odbexport.export.static(folder_odb,jobname,folder_save,folder_python,stepnumber=-2,framenumber=-1)