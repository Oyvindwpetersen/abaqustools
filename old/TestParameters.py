

import numpy as np
from ypstruct import *
import numpy as np
import numtools
import gen
import warnings
import os


abaqus=struct()

abaqus.FolderNameModel='C:/Cloud/OD_OWP/Work/Github/abaqustools/TestModel'
abaqus.InputName='TestInput'
abaqus.JobName='TestJob'
abaqus.PartName='MyPartName'
abaqus.AssemblyName='MyAssembly'
abaqus.RunJob=True
abaqus.cmd='abaqus'
abaqus.cpus=np.array(4)
abaqus.restart=False
abaqus.halt_error=True


##########################
##########################
##########################

step=struct()

step.time=[None]*4
step.time[0]=np.array([1e-3, 1, 1e-6, 1])
step.time[1]=np.array([1e-8, 1, 1e-12, 1])
step.time[2]=np.array([1e-6, 1, 1e-9, 1])
step.time[3]=np.array([1e-1, 1, 1e-6, 1])


##########################
##########################
##########################

modal=struct()
modal.N_modes=np.array(100)
modal.normalization='displacement'

##########################
##########################
##########################

cable=struct()
cable.cs=struct()

cable.cs.A=np.array(0.6)
cable.cs.I11=np.array(1e-6)
cable.cs.I22=np.array(1e-6)
cable.cs.I12=np.array(0)
cable.cs.It=np.array(1e-5)
cable.cs.rho=np.array(7850)
cable.cs.E=np.array(200e9)
cable.cs.G=np.array(80e9)
cable.cs.sigma_target=np.nan


cable.normaldir=np.array([0,1,0])
cable.eltype='B33'

cable.meshsize_approx=np.nan
cable.N_element=np.array(50)
cable.tempsupport=True
cable.N_tempsupport=np.array(9)
cable.NodeNumberBase=np.array([10e3,20e3])
cable.ElementNumberBase=np.array([10e3,20e3])
cable.polycoeff_hanger_adjust=np.nan



##########################
##########################
##########################


bridgedeck=struct()
bridgedeck.cs=struct()
bridgedeck.inertia=struct()
bridgedeck.gapbeam=struct()

bridgedeck.cs.A=np.array([0.7])
bridgedeck.cs.I11=np.array([0.6])
bridgedeck.cs.I22=np.array([17])
bridgedeck.cs.I12=np.array([0])
bridgedeck.cs.It=np.array([1.5])
bridgedeck.cs.rho=np.array([0])
bridgedeck.cs.E=np.array([210e9])
bridgedeck.cs.G=np.array([81e9])
bridgedeck.cs.sc1=np.array([0])
bridgedeck.cs.sc2=np.array([0])


bridgedeck.inertia.m=np.array([9000])
bridgedeck.inertia.x1=np.array([0])
bridgedeck.inertia.x2=np.array([0])
bridgedeck.inertia.alpha=np.array([0])
bridgedeck.inertia.I11=np.array([10e3])
bridgedeck.inertia.I22=np.array([200e3])
bridgedeck.inertia.I12=np.array([0])

bridgedeck.N_box=1

bridgedeck.normaldir=np.array([0,1,0])
bridgedeck.eltype='B31'
bridgedeck.meshsize=np.array(4)
bridgedeck.shell=True


bridgedeck.gapbeam.type='box'
bridgedeck.gapbeam.h=np.array(2)
bridgedeck.gapbeam.b=np.array(2)
bridgedeck.gapbeam.t=np.array(0.02)

bridgedeck.NodeNumberBase=np.array([1e3,2e3,3e3,4e3,5e3])
bridgedeck.ElementNumberBase=np.array([1e3,2e3])

bridgedeck.NodeNumberBaseOuter=np.array([11e3,12e3])
bridgedeck.ElementNumberBaseConnLat=np.array([3e3,4e3,5e3,6e3,7e3,8e3])



##########################
##########################
##########################


hanger=struct()
hanger.cs=struct()


hanger.cs.A=np.array(4e-3)
hanger.cs.I11=np.array(1e-7)
hanger.cs.I22=np.array(1e-7)
hanger.cs.I12=np.array(0)
hanger.cs.It=np.array(1e-7)
hanger.cs.rho=np.array(7850)
hanger.cs.E=np.array(160e9)
hanger.cs.G=np.array(60e9)

hanger.normaldir=np.array([0,1,0])
hanger.eltype='B31'
hanger.ElementNumberBase=np.array([80e3,90e3])



##########################
##########################
##########################


tower=struct()
tower.cs=struct()

tower.cs.type='box'
tower.cs.h_vec=np.array([10,8,7])
tower.cs.b_vec=np.array([10,8,7])
tower.cs.t_vec=np.array([1.5,1.5,1.5])
tower.cs.z_vec=np.array([50,75,200])
tower.cs.rho=np.array(2500)
tower.cs.E=np.array(35e9)
tower.cs.v=np.array(0.2)

tower.normaldir=np.array([0,1,0])
tower.eltype='B31'

tower.F_pullback_south=np.array(-3e3) #np.nan
tower.F_pullback_north=np.array(3e3) #np.nan

tower.z_crossbeam_south=np.array([40,70,130])
tower.z_crossbeam_north=np.array([40,70,130])

tower.h_crossbeam=np.array([8,8,8])
tower.b_crossbeam=np.array([8,8,8])
tower.t_crossbeam=np.array([1,1,1])

tower.N_element=np.nan
tower.meshsize=np.array(5)

tower.NodeNumberBase=np.array([100e3,110e3,200e3,210e3])
tower.ElementNumberBase=np.array([100e3,110e3,200e3,210e3])


##########################
##########################
##########################


bearing=struct()

bearing.type='tri'
bearing.stiffness_south=np.array([3e7,1e12,1e6,1e0,1e0,1e0])
bearing.stiffness_north=np.array([3e7,1e12,1e6,1e0,1e0,1e0])
bearing.NodeNumberBase=np.array([400e3])
bearing.ElementNumberBase=np.array([400e3])


##########################
##########################
##########################


sadle=struct()

sadle.stiffness=np.array([1e12])
sadle.ElementNumberBase=np.array([300e3])


##########################
##########################
##########################


geo=struct()

geo.L_bridgedeck=np.array(1000)
geo.gap=np.nan

geo.dx_hanger=np.array(24)
geo.dx_endpiece_max=np.array(24)

geo.dx_pullback_south=np.array(-1)
geo.dx_pullback_north=np.array(1)

geo.z_cog_south=np.array(57.5)
geo.z_cog_north=np.array(57.5)
geo.z_cog_midspan=np.array(76)
geo.dz_cog_midspan_deflection=np.array(15)
geo.dz_cog_south_deflection=np.array(1)
geo.dz_cog_north_deflection=np.array(1)

geo.z_cable_top_south=np.array(200+0.1)
geo.z_cable_top_north=np.array(200+0.1)
geo.z_cable_midspan=np.array(80)
geo.dz_cable_deflection=np.array(30)

geo.dy_cable_anch_south=np.array(52)
geo.dy_cable_top_south=np.array(47)
geo.dy_cable_midspan=np.array(47)
geo.dy_cable_top_north=np.array(47)
geo.dy_cable_anch_north=np.array(52)

geo.dy_cog_hanger=np.array(8)
geo.dz_cog_hanger=np.array(0.3)
geo.dy_cog_inner=np.array(8)
geo.dz_cog_inner=np.array(-0.5)

geo.dy_pendulum=np.array(1)
geo.dz_slider=np.array(-2)
geo.dx_bearing_base=np.array(1)

geo.z_tower_base_south=np.array(10)
geo.z_tower_base_north=np.array(10)

geo.z_tower_top_south=np.array(200)
geo.z_tower_top_north=np.array(200)

geo.dy_tower_base_south=np.array(40)
geo.dy_tower_base_north=np.array(40)

geo.dy_tower_top_south=np.array(20)
geo.dy_tower_top_north=np.array(20)

geo.dx_tower_anch_south=np.array(500)
geo.dx_tower_anch_north=np.array(500)

geo.z_anch_south=np.array(50)
geo.z_anch_north=np.array(50)

geo.x_tower_south=np.array(-500)
geo.x_tower_north=np.array(500)

