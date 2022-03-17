
#%%

import sys

sys.path.append('C:/Cloud/OD_OWP/Work/Python/Github')

# import abaqustools
from abaqustools import suspensionbridge

from abaqustools import odbexport

#%%

UserParameterFolder='C:\\Cloud\\OD_OWP\\Work\\Python\\Github\\abaqustools\\example_suspensionbridge'
#UserParameterFileName='LangenuenParameters.py'
UserParameterFileName='SulafjordenParameters.py'

suspensionbridge.MainSuspensionBridge(UserParameterFileName,UserParameterFolder,IterateDeflection=True)


#%%

# FolderODB='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/TestModel'
# NameODB='TestLangenuen'
# FolderSave=FolderODB
# FolderPython='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport'

# odbexport.exportmodal.exportmodal(FolderODB,NameODB,FolderSave,FolderPython)

