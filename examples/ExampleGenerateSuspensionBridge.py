

import sys

sys.path.append('C:/Cloud/OD_OWP/Work/Python/Github/abaqustools')



#%%

import suspensionbridge


#%%

UserParameterFolder='C://Cloud//OD_OWP/Work//Python//Github//abaqustools//examples'
UserParameterFileName='LangenuenParameters.py'
UserParameterFileName='SulafjordenParameters.py'

suspensionbridge.MainSuspensionBridge(UserParameterFileName,UserParameterFolder)
