# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2017 replay file
# Internal Version: 2016_09_27-23.54.59 126836
# Run by oyvinpet on Mon Feb 28 15:14:10 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=196.511627197266, 
    height=52.809024810791)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
o2 = session.openOdb(name='TestLangenuen.odb')
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/TestModel/TestLangenuen.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       144
#: Number of Node Sets:          47
#: Number of Steps:              5
session.viewports['Viewport: 1'].setValues(displayedObject=o2)
