
import os
import numpy as np

FolderODB='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/example_suspensionbridge/Sulafjorden'
JobName='TestSulafjorden'
FolderSave='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/example_suspensionbridge/Sulafjorden'
FolderPython='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport'
Prefix='TestSulafjorden_export_'

# Import functions for export
CurrentDir=os.getcwd()
os.chdir(FolderPython)
import odbfunc
os.chdir(CurrentDir)

# Open ODB
myOdb=odbfunc.OpenODB(FolderODB,'TestSulafjorden')

# Frequencies
freq=odbfunc.Export_HistoryOutput(myOdb,-1,'EIGFREQ')
odbfunc.SaveToTXT(FolderSave,'freq',freq,atype=1,Prefix=Prefix)

# Generalized mass
genmass=odbfunc.Export_HistoryOutput(myOdb,-1,'GM')
odbfunc.SaveToTXT(FolderSave,'genmass',genmass,atype=1,Prefix=Prefix)

# Mode shapes
(phi,phi_label)=odbfunc.Export_U_UR(myOdb,-1,FrameNumber='skipfirst')
odbfunc.SaveToTXT(FolderSave,'phi',phi,atype=1,Prefix=Prefix)
odbfunc.SaveToTXT(FolderSave,'phi_label',phi_label,atype=2,Prefix=Prefix)

# Modal section forces
(phi_sf,phi_sf_label)=odbfunc.Export_SectionForce(myOdb,-1,FrameNumber='skipfirst')
odbfunc.SaveToTXT(FolderSave,'phi_sf',phi_sf,atype=1,Prefix=Prefix)
odbfunc.SaveToTXT(FolderSave,'phi_sf_label',phi_sf_label,atype=2,Prefix=Prefix)

# Node coordinates
nodecoord=odbfunc.Export_NodeCoord(myOdb,-1,0)
odbfunc.SaveToTXT(FolderSave,'nodecoord',nodecoord,atype=1,Prefix=Prefix)

# Close ODB
odbfunc.CloseODB(myOdb)
