
import os
import numpy as np

FolderODB='C:\Cloud\OD_OWP\Work\Python\Github\abaqustools\TestModel'
JobName='TestLangenuen'
FolderSave='C:\Cloud\OD_OWP\Work\Python\Github\abaqustools\TestModel'
FolderPython='C:\Cloud\OD_OWP\Work\Python\Github\abaqustools\odbexport'
Prefix='TestLangenuen'

# Import functions for export
CurrentDir=os.getcwd()
os.chdir(FolderPython)
import odbfunc
os.chdir(CurrentDir)


# Open ODB
myOdb=odbfunc.OpenODB(FolderODB,'TestLangenuen')

# Frequencies
freq=odbfunc.Export_HistoryOutput(myOdb,-1,'EIGFREQ')
odbfunc.SaveToTXT(FolderSave,'freq',freq,atype=1,Prefix=Prefix)

# Mass
genmass=odbfunc.Export_HistoryOutput(myOdb,-1,'GM')
odbfunc.SaveToTXT(FolderSave,'genmass',genmass,atype=1,Prefix=Prefix)

# Mode shapes
(Phi,Phi_Label)=odbfunc.Export_U_UR(myOdb,-1,FrameNumber='skipfirst')
odbfunc.SaveToTXT(FolderSave,'Phi',Phi,atype=1,Prefix)
odbfunc.SaveToTXT(FolderSave,'Phi_Label',Phi_Label,atype=2,Prefix=Prefix)

# Node coordinates
(NodeCoord,NodeNumbers)=odbfunc.Export_NodeCoord(myOdb,-1,0)
odbfunc.SaveToTXT(FolderSave,'NodeCoord',NodeCoord,atype=1,Prefix)
odbfunc.SaveToTXT(FolderSave,'NodeNumbers',NodeNumbers,atype=1,Prefix=Prefix)

(Phi_SF,Phi_SF_Label)=odbfunc.Export_NodeCoord(myOdb,-1)
odbfunc.SaveToTXT(FolderSave,'Phi_SF',Phi_SF,atype=1,Prefix)
odbfunc.SaveToTXT(FolderSave,'Phi_SF_Label',Phi_SF_Label,atype=2,Prefix=Prefix)

odbfunc.CloseODB(myOdb)
