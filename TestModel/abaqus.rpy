# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2017 replay file
# Internal Version: 2016_09_27-23.54.59 126836
# Run by oyvinpet on Thu Feb 10 13:11:03 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=307.999969482422, 
    height=173.0)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
o2 = session.openOdb(name='TestSulafjorden.odb')
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/TestModel/TestSulafjorden.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       244
#: Number of Node Sets:          85
#: Number of Steps:              5
session.viewports['Viewport: 1'].setValues(displayedObject=o2)
import sys
sys.path.insert(15, r'c:/Users/oyvinpet/abaqus_plugins/ModalViewPlugin')
import ModalView
import ModalView
ModalView.ModalViewFunc(DoRenderBeamProfiles='No', deflection=50, 
    X_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=1806.69, 
    farPlane=4998.91, width=69.4167, height=31.9678, viewOffsetX=-737.246, 
    viewOffsetY=-224.694)
session.viewports['Viewport: 1'].view.setValues(nearPlane=1805.89, 
    farPlane=4999.7, width=69.3861, height=31.9537, viewOffsetX=-729.154, 
    viewOffsetY=-214.855)
session.viewports['Viewport: 1'].view.setValues(nearPlane=1813.31, 
    farPlane=4992.28, width=29.2984, height=13.4925, viewOffsetX=-738.928, 
    viewOffsetY=-213.514)
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].view.setValues(nearPlane=1225.6, 
    farPlane=5579.99, width=2915.49, height=1342.64, viewOffsetX=454.427, 
    viewOffsetY=-75.7734)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3532.56, 
    farPlane=5067.65, width=10505.3, height=3869.9, cameraPosition=(419.879, 
    -3832, 2144.1), cameraUpVector=(0.317404, 0.745427, 0.586168), 
    cameraTarget=(-269.762, -573.848, 505.384), viewOffsetX=1309.8, 
    viewOffsetY=-218.402)
session.viewports['Viewport: 1'].view.setValues(nearPlane=2606.32, 
    farPlane=5674.68, width=7750.8, height=2855.21, cameraPosition=(1209.25, 
    -2670.34, 3219.33), cameraUpVector=(-0.211251, 0.933204, 0.290695), 
    cameraTarget=(-293.257, -791.359, 392.947), viewOffsetX=966.368, 
    viewOffsetY=-161.137)
session.viewports['Viewport: 1'].view.setValues(nearPlane=2690.25, 
    farPlane=5590.74, width=8000.42, height=2947.16, cameraPosition=(1219.78, 
    -2955.56, 3024.12), cameraUpVector=(-0.398794, 0.852877, 0.336992), 
    cameraTarget=(-282.728, -1076.58, 197.735), viewOffsetX=997.489, 
    viewOffsetY=-166.326)
session.viewports['Viewport: 1'].view.setValues(nearPlane=2741.71, 
    farPlane=5756.26, width=8153.46, height=3003.53, cameraPosition=(1374.34, 
    -3250.44, 2769.26), cameraUpVector=(-0.352399, 0.830154, 0.432041), 
    cameraTarget=(-254.091, -1106.92, 213.851), viewOffsetX=1016.57, 
    viewOffsetY=-169.507)
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/TestModel/TestSulafjorden.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
