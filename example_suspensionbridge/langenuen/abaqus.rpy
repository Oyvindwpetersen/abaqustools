# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2017 replay file
# Internal Version: 2016_09_27-23.54.59 126836
# Run by oyvinpet on Thu Mar 17 10:29:32 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=238.509353637695, 
    height=152.491668701172)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
o2 = session.openOdb(name='TestLangenuen.odb')
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example_suspensionbridge/langenuen/TestLangenuen.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       144
#: Number of Node Sets:          47
#: Number of Steps:              5
session.viewports['Viewport: 1'].setValues(displayedObject=o2)
import sys
sys.path.insert(15, r'c:/Users/oyvinpet/abaqus_plugins/ModalViewPlugin')
import ModalView
import ModalView
ModalView.ModalViewFunc(DoRenderBeamProfiles='No', deflection=50, 
    X_in_or_out='In')
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='STEP1', frame=1)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='STEP2', frame=1)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='STEP3', frame=1)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='STEP4', frame=1)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='STEP_MODAL', 
    frame=1)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='STEP_MODAL', 
    frame=2)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='STEP_MODAL', 
    frame=3)
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Projects/Sulafjorden/SulafjordenModel_20210929/SulafjordenModel_S2_G3.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Projects/Sulafjorden/SulafjordenModel_20210929/SulafjordenModel_S2_G3.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       242
#: Number of Node Sets:          85
#: Number of Steps:              5
import ModalView
ModalView.ModalViewFunc(DoRenderBeamProfiles='No', deflection=50, 
    X_in_or_out='In')
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
