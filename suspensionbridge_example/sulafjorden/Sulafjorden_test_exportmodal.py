
import os
import sys
import numpy as np

foldername_odb='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/suspensionbridge_example/sulafjorden'
jobname='Sulafjorden_test'
folder_save='C:/Cloud\OD_OWP/Work/Python/Github/abaqustools/suspensionbridge_example/sulafjorden'
folder_python='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport'
prefix='Sulafjorden_test_export_'

# Import functions for export (odbexport package)
sys.path.append(folder_python)
import odbfunc

# Open ODB
odb_id=odbfunc.open_odb(foldername_odb,jobname)

# Step and frames to export
stepnumber=-1
framenumber='skipfirst'

# Frequencies
f=odbfunc.exporthistoryoutput(odb_id,stepnumber,'EIGFREQ')
odbfunc.save2txt(folder_save,'f',f,atype=1,prefix=prefix)

# Generalized mass
gm=odbfunc.exporthistoryoutput(odb_id,stepnumber,'GM')
odbfunc.save2txt(folder_save,'gm',gm,atype=1,prefix=prefix)

# Mode shapes
(phi,phi_label)=odbfunc.exportdisplacement(odb_id,stepnumber,framenumber=framenumber)
odbfunc.save2txt(folder_save,'phi',phi,atype=1,prefix=prefix)
odbfunc.save2txt(folder_save,'phi_label',phi_label,atype=2,prefix=prefix)

# Modal section forces
(phi_sf,phi_sf_label)=odbfunc.exportsectionforce(odb_id,stepnumber,framenumber=framenumber)
odbfunc.save2txt(folder_save,'phi_sf',phi_sf,atype=1,prefix=prefix)
odbfunc.save2txt(folder_save,'phi_sf_label',phi_sf_label,atype=2,prefix=prefix)

# Node coordinates
nodecoord=odbfunc.exportnodecoord(odb_id,stepnumber,0)
odbfunc.save2txt(folder_save,'nodecoord',nodecoord,atype=1,prefix=prefix)

# Element connectivity
elconn=odbfunc.exportelconn(odb_id)
odbfunc.save2txt(folder_save,'elconn',elconn,atype=1,prefix=prefix)

# Close ODB
odbfunc.close_odb(odb_id)
