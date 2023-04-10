
import os
import sys
import numpy as np

FolderODB='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/suspensionbridge_example/langenuen'
JobName='Langenuen_test'
FolderSave='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/suspensionbridge_example/langenuen'
FolderPython='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport'
prefix='Langenuen_test_export_'

# Import functions for export
sys.path.append(FolderPython)
import odbfunc

# Open ODB
myOdb=odbfunc.open_odb(FolderODB,'Langenuen_test')

# Step and frames to export
StepNumber=-1
FrameNumber='skipfirst'

# Frequencies
f=odbfunc.exporthistoryoutput(myOdb,StepNumber,'EIGFREQ')
odbfunc.save2txt(FolderSave,'f',f,atype=1,prefix=prefix)

# Generalized mass
gm=odbfunc.exporthistoryoutput(myOdb,StepNumber,'GM')
odbfunc.save2txt(FolderSave,'gm',gm,atype=1,prefix=prefix)

# Mode shapes
(phi,phi_label)=odbfunc.exportdisplacement(myOdb,StepNumber,FrameNumber=FrameNumber)
odbfunc.save2txt(FolderSave,'phi',phi,atype=1,prefix=prefix)
odbfunc.save2txt(FolderSave,'phi_label',phi_label,atype=2,prefix=prefix)

# Modal section forces
(phi_sf,phi_sf_label)=odbfunc.exportsectionforce(myOdb,StepNumber,FrameNumber=FrameNumber)
odbfunc.save2txt(FolderSave,'phi_sf',phi_sf,atype=1,prefix=prefix)
odbfunc.save2txt(FolderSave,'phi_sf_label',phi_sf_label,atype=2,prefix=prefix)

# Node coordinates
nodecoord=odbfunc.exportnodecoord(myOdb,StepNumber,0)
odbfunc.save2txt(FolderSave,'nodecoord',nodecoord,atype=1,prefix=prefix)

# Element connectivity
elconn=odbfunc.exportelconn(myOdb)
odbfunc.save2txt(FolderSave,'elconn',elconn,atype=1,prefix=prefix)

# Close ODB
odbfunc.close_odb(myOdb)
