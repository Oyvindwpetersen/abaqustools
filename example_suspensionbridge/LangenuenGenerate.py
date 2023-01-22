# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:36:35 2022

@author: oyvinpet
"""

#%%

import sys

sys.path.append('C:/Cloud/OD_OWP/Work/Python/Github')

# import abaqustools
from abaqustools import suspensionbridge

from abaqustools import odbexport

#%%

UserParameterFolder='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/example_suspensionbridge'
UserParameterFileName='LangenuenParameters.py'

suspensionbridge.MainSuspensionBridge(UserParameterFileName,UserParameterFolder,IterateDeflection=False)


#%%

FolderODB='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/example_suspensionbridge/langenuen'
NameODB='TestLangenuen'
FolderSave=FolderODB
FolderPython='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport'

odbexport.exportmodal.exportmodal(FolderODB,NameODB,FolderSave,FolderPython)


