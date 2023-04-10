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

UserParameterFolder=r'C:\Cloud\OD_OWP\Work\Python\Github\abaqustools\suspensionbridge_example'
UserParameterFileName='LangenuenParameters.py'

suspensionbridge.model.buildinput(UserParameterFileName,UserParameterFolder,IterateDeflection=False)


#%%

FolderODB='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/suspensionbridge_example/langenuen'
NameODB='Langenuen_test'
FolderSave=FolderODB
FolderPython='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport'

odbexport.export.modal(FolderODB,NameODB,FolderSave,FolderPython)


