# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2017 replay file
# Internal Version: 2016_09_27-23.54.59 126836
# Run by oyvinpet on Fri Mar 04 13:14:21 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.16279, 1.16319), width=171.163, 
    height=115.389)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile(
    'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/TestModel/ExportModal.py', 
    __main__.__dict__)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/TestModel/TestLangenuen.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       144
#: Number of Node Sets:          47
#: Number of Steps:              5
#: Time displacement 4.1162895 s
#: Time nodecoord 0.032425 s
print 'RT script done'
#: RT script done
