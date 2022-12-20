# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2017 replay file
# Internal Version: 2016_09_27-23.54.59 126836
# Run by oyvinpet on Thu May 05 15:00:49 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=342.558135986328, 
    height=72.3506927490234)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
o2 = session.openOdb(name='TestSmallBridge.odb')
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example_suspensionbridge/asmallbridge/TestSmallBridge.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       102
#: Number of Node Sets:          57
#: Number of Steps:              5
session.viewports['Viewport: 1'].setValues(displayedObject=o2)
import sys
sys.path.insert(15, r'c:/Users/oyvinpet/abaqus_plugins/ModalViewPlugin')
import ModalView
import ModalView
ModalView.ModalViewFunc(DoRenderBeamProfiles='No', deflection=50, 
    X_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=3344.01, 
    farPlane=3532.62, width=160.631, height=83.8412, viewOffsetX=-21.2982, 
    viewOffsetY=-102.252)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    uniformScaleFactor=5)
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3357.61, 
    farPlane=3518.55, width=126.438, height=65.9941, viewOffsetX=-33.1338, 
    viewOffsetY=-102.3)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=16 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=17 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=16 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=16 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=17 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=18 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=19 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=20 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=21 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=22 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=23 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=24 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=25 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=26 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=27 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=28 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=29 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=30 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=31 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=32 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=33 )
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='STEP4', frame=1)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='SF', outputPosition=INTEGRATION_POINT, refinement=(
    COMPONENT, 'SF1'), )
#: 
#: Element: SUSPENSIONBRIDGE.10045
#:   Type: B33
#:   Material: 
#:   Section: 
#:   Connect: 10045, 10046
#:   SF, SF1 (Not averaged): 1.42503e+06, 1.42507e+06, 1.42511e+06
#: 
#: Element: SUSPENSIONBRIDGE.10052
#:   Type: B33
#:   Material: 
#:   Section: 
#:   Connect: 10052, 10053
#:   SF, SF1 (Not averaged): 1.50937e+06, 1.50923e+06, 1.50873e+06
session.viewports['Viewport: 1'].view.setValues(nearPlane=3359.15, 
    farPlane=3516.37, width=111.771, height=58.3391, viewOffsetX=-35.498, 
    viewOffsetY=-102.156)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
#: 
#: Node: SUSPENSIONBRIDGE.12007
#:                                         1             2             3        Magnitude
#: Base coordinates:                 -4.40000e+001,  2.00000e+000,  3.93280e-001,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: SUSPENSIONBRIDGE.1005
#:                                         1             2             3        Magnitude
#: Base coordinates:                 -4.60000e+001,  0.00000e+000,  1.99680e-001,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: SUSPENSIONBRIDGE.1027
#:                                         1             2             3        Magnitude
#: Base coordinates:                 -2.40000e+001,  0.00000e+000,  1.00048e+000,      -      
#: No deformed coordinates for current plot.
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    renderBeamProfiles=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3253.26, 
    farPlane=3622.39, width=991.912, height=517.728, viewOffsetX=105.072, 
    viewOffsetY=-66.1758)
leaf = dgo.LeafFromElementSets(elementSets=('SUSPENSIONBRIDGE.BRIDGEDECK_COG', 
    ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
