from sys import path
import numpy as np
import odbAccess
from abaqusConstants import *
import os
from textRepr import *
from numpy import genfromtxt
import visualization
import animation
import displayGroupOdbToolset as dgo 

def p(pstring):
    prettyPrint(pstring)

# 

foldername_print=r'C:\Cloud\OD_OWP\Work\Projects\Long_span_bridges\Langenuen\Abaqus\PlotModel'

cameraPosition=(-1250, -900, 600)
cameraUpVector=(0.43, 0.43, 0.78)
nearPlane=1338
cameraTarget= (200, 0, 100)
fieldOfViewAngle=80
viewOffsetX=-100
viewOffsetY=-50

initialcolor_model='#0009FF'
initialcolor_modes='#BDBDBD'

mode_print=np.array([1,2,3,4,5,6,    7,8,9])
scalefactor=np.array([-1 , 1, 1, 1, 1 , 0.8     , 1, 1,1])*1e2

filename_model='Langenuen_model'
filename_mode='Langenuen_mode_'

png_size_model=(2000, 560)
png_size_modes=(1000, 280)

# Viewport
viewport_obj = session.viewports[session.currentViewportName]
odb_obj=viewport_obj.displayedObject

viewport_obj.viewportAnnotationOptions.setValues(
	triad=OFF, title=OFF, state=OFF, compass=OFF, legend=OFF,
	legendBox=0,
	legendDecimalPlaces= 2,
	triadPosition= (3, 4),
	legendFont='-*-verdana-medium-r-normal-*-*-80-*-*-p-*-*-*', 
	titleFont='-*-verdana-medium-r-normal-*-*-120-*-*-p-*-*-*', 
	stateFont='-*-verdana-medium-r-normal-*-*-80-*-*-p-*-*-*')
	

# Set last step
stepkeys=odb_obj.steps.keys()

viewport_obj.odbDisplay.setFrame(step=stepkeys[-1], frame=0)
firstframe=odb_obj.steps[stepkeys[-1]].frames[0]
dispfield=firstframe.fieldOutputs['U']
viewport_obj.odbDisplay.setPrimaryVariable(field=dispfield,outputPosition=NODAL,refinement=(INVARIANT, 'Magnitude'))

# View
viewport_obj.odbDisplay.basicOptions.setValues(beamScaleFactor=1.0, renderBeamProfiles=OFF, shellScaleFactor=1.0, renderShellThickness=OFF,
	referencePoints=OFF)
viewport_obj.odbDisplay.commonOptions.setValues(deformationScaling=UNIFORM, uniformScaleFactor=1,visibleEdges=NONE)
viewport_obj.odbDisplay.display.setValues(plotState=(UNDEFORMED)) #UNDEFORMED

viewport_obj.view.setValues(cameraPosition=cameraPosition)
viewport_obj.view.setValues(cameraUpVector=cameraUpVector)
viewport_obj.view.setValues(nearPlane=nearPlane)
viewport_obj.view.setValues(cameraTarget=cameraTarget)
viewport_obj.view.setValues(fieldOfViewAngle=fieldOfViewAngle)
viewport_obj.view.setValues(viewOffsetX=viewOffsetX)
viewport_obj.view.setValues(viewOffsetY=viewOffsetY)


# Print model with initial color
viewport_obj.odbDisplay.commonOptions.setValues(deformationScaling=UNIFORM, uniformScaleFactor=0,visibleEdges=NONE)
viewport_obj.setColor(initialColor=initialcolor_model)

# Set size
session.pngOptions.setValues(imageSize=png_size_model)

session.printToFile(fileName=foldername_print + '/' +filename_model,format=PNG, canvasObjects=(viewport_obj, ))


# Print modes
viewport_obj.setColor(initialColor=initialcolor_modes)
viewport_obj.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF,UNDEFORMED))

viewport_obj.odbDisplay.superimposeOptions.setValues(edgeColorFillShade=initialcolor_modes,renderStyle=WIREFRAME) 
viewport_obj.odbDisplay.contourOptions.setValues(spectrum='Blue to red',numIntervals=20, maxAutoCompute=ON, minAutoCompute=ON) 

# Set size
session.pngOptions.setValues(imageSize=png_size_modes)

for k in range(len(mode_print)):
	
	viewport_obj.odbDisplay.setFrame(step=stepkeys[-1], frame=mode_print[k])
	# viewport_obj.odbDisplay.setDeformedVariable(dispfield)
	viewport_obj.odbDisplay.commonOptions.setValues(deformationScaling=UNIFORM, uniformScaleFactor=scalefactor[k])
    
	session.printToFile(foldername_print + '/' + filename_mode + str(mode_print[k]),format=PNG, canvasObjects=(viewport_obj, ))
