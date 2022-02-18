# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2017 replay file
# Internal Version: 2016_09_27-23.54.59 126836
# Run by oyvinpet on Fri Feb 18 12:38:22 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=222.093017578125, 
    height=89.1006927490234)
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
session.viewports['Viewport: 1'].view.setValues(nearPlane=3169.76, 
    farPlane=4836.39, width=2134.86, height=716.978, cameraPosition=(2891.69, 
    -193.977, 2865.82), cameraUpVector=(0.162936, 0.786245, -0.596046), 
    cameraTarget=(78.09, -46.8205, 71.7475))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3477.66, 
    farPlane=4463.17, width=2342.24, height=786.623, cameraPosition=(-1231.56, 
    -2364.48, 3046.43), cameraUpVector=(0.894986, 0.380577, 0.232726), 
    cameraTarget=(41.9469, -65.8464, 73.3307))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3035.12, 
    farPlane=4891.72, width=2044.19, height=686.525, cameraPosition=(-3449, 
    -1954.39, 82.4633), cameraUpVector=(0.386616, -0.00866444, 0.9222), 
    cameraTarget=(40.5849, -65.5945, 71.51))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3050.1, 
    farPlane=4876.75, width=2054.28, height=689.915, cameraPosition=(-3449, 
    -1954.39, 82.4633), cameraUpVector=(0.268612, 0.209454, 0.9402), 
    cameraTarget=(40.5849, -65.5945, 71.51))
session.viewports['Viewport: 1'].view.setValues(nearPlane=2993.3, 
    farPlane=4900.34, width=2016.03, height=677.068, cameraPosition=(-3521.32, 
    -1488.99, 1086.51), cameraUpVector=(0.448036, 0.384406, 0.807153), 
    cameraTarget=(40.668, -66.1294, 70.3559))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3056.79, 
    farPlane=4836.85, width=921.032, height=309.322, viewOffsetX=-169.327, 
    viewOffsetY=-87.0031)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3053.93, 
    farPlane=4839.72, width=920.168, height=309.032, viewOffsetX=-140.648, 
    viewOffsetY=9.18164)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3062.18, 
    farPlane=4831.46, width=720.363, height=241.928, viewOffsetX=-161.917, 
    viewOffsetY=0.128155)
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    renderBeamProfiles=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3038.64, 
    farPlane=4854.86, width=1247.52, height=418.972, viewOffsetX=-71.0783, 
    viewOffsetY=-20.6492)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3034.8, 
    farPlane=4858.7, width=1245.95, height=418.442, cameraPosition=(-3521.92, 
    -1493.79, 1077.67), cameraUpVector=(0.487827, 0.295079, 0.821555), 
    cameraTarget=(40.0657, -70.9343, 61.5165), viewOffsetX=-70.9885, 
    viewOffsetY=-20.6231)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3034.8, 
    width=1245.95, height=418.442, viewOffsetX=-144.973, viewOffsetY=-71.0476)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3055.19, 
    farPlane=4838.31, width=813.398, height=273.174, viewOffsetX=-190.902, 
    viewOffsetY=-93.9565)
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    renderBeamProfiles=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3096.22, 
    farPlane=4797.41, width=121.077, height=40.6628, viewOffsetX=-276.331, 
    viewOffsetY=-1.85082)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3116.99, 
    farPlane=4693.75, width=121.889, height=40.9355, cameraPosition=(-3186.7, 
    -1895.94, 1331.86), cameraUpVector=(0.537144, 0.323053, 0.779175), 
    cameraTarget=(59.7675, -30.7226, 18.0022), viewOffsetX=-278.185, 
    viewOffsetY=-1.86323)
session.viewports['Viewport: 1'].view.setValues(viewOffsetX=-302.677, 
    viewOffsetY=-16.3038)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3133.07, 
    farPlane=4590.8, width=122.518, height=41.1467, cameraPosition=(-2890.69, 
    -2218.01, 1387.11), cameraUpVector=(0.55928, 0.329961, 0.760481), 
    cameraTarget=(75.0607, 10.1889, -21.528), viewOffsetX=-304.243, 
    viewOffsetY=-16.3882)
session.viewports['Viewport: 1'].view.setValues(viewOffsetX=-337.217, 
    viewOffsetY=-24.3054)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3047.55, 
    farPlane=4676.32, width=1828.53, height=614.096, viewOffsetX=257.072, 
    viewOffsetY=-103.984)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3042.03, 
    farPlane=4681.84, width=1825.21, height=612.984, viewOffsetX=117.854, 
    viewOffsetY=40.9614)
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/TestModel/TestLangenuen.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
