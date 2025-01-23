
import os
import sys
import numpy as np

folder_odb='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport_example'
jobname='Model_single_deck'
folder_save='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport_example'
folder_python='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport'
prefix='Model_single_deck_export_'

# Import functions for export (odbexport package)
sys.path.append(folder_python)
import odbfunc

# Open ODB
odb_id=odbfunc.open_odb(folder_odb,jobname)

# Step and frames to export
stepnumber=-2
framenumber=-1

# Node numbers to export
nodes=None

# Displacements
(u,u_label)=odbfunc.exportdisplacement(odb_id,stepnumber,framenumber=framenumber,nodes=nodes)
odbfunc.save2txt(folder_save,'u',u,atype=1,prefix=prefix)
odbfunc.save2txt(folder_save,'u_label',u_label,atype=2,prefix=prefix)

# Section forces
(sf,sf_label)=odbfunc.exportsectionforce(odb_id,stepnumber,framenumber=framenumber)
odbfunc.save2txt(folder_save,'sf',sf,atype=1,prefix=prefix)
odbfunc.save2txt(folder_save,'sf_label',sf_label,atype=2,prefix=prefix)

# Node coordinates
nodecoord=odbfunc.exportnodecoord(odb_id,stepnumber,0)
odbfunc.save2txt(folder_save,'nodecoord',nodecoord,atype=1,prefix=prefix)

# Element connectivity
elconn=odbfunc.exportelconn(odb_id)
odbfunc.save2txt(folder_save,'elconn',elconn,atype=1,prefix=prefix)

# Element sets
(elset,elset_label)=odbfunc.exportelsets(odb_id)
odbfunc.save2txt(folder_save,'elset',elset,atype=1,prefix=prefix)
odbfunc.save2txt(folder_save,'elset_label',elset_label,atype=2,prefix=prefix)

# Close ODB
odbfunc.close_odb(odb_id)
