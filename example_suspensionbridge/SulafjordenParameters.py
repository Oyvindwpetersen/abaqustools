
import numpy as np
from ypstruct import *

##########################
##########################
##########################

abaqus=struct()

abaqus.FolderNameModel='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example_suspensionbridge/sulafjorden'
abaqus.InputName='TestSulafjorden'
abaqus.JobName='TestSulafjorden'
abaqus.PartName='SuspensionBridge'
abaqus.AssemblyName='AssemblySuspensionBridge'
abaqus.RunJob=True
abaqus.cmd='abaqus'
abaqus.cpus=np.array(4)
abaqus.restart=False
abaqus.halt_error=True
abaqus.FolderODBExport='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/odbexport'

##########################
##########################
##########################

step=struct()

step.time=[None]*4
step.time[0]=np.array([1e-1, 1, 1e-6, 1])
step.time[1]=np.array([1e-6, 1, 1e-12, 1])
step.time[2]=np.array([1e-4, 1, 1e-9, 1])
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
cable.cs.I11=cable.cs.A**2/(4*np.pi)*0.01
cable.cs.I22=cable.cs.A**2/(4*np.pi)*0.01
cable.cs.I12=np.array(0)
cable.cs.It=cable.cs.A**2/(2*np.pi)*0.01
cable.cs.rho=np.array(7850)
cable.cs.E=np.array(200e9)
cable.cs.G=np.array(80e9)
cable.cs.sigma_target=np.nan

cable.normaldir=np.array([0,1,0])
cable.eltype='B33'
cable.meshsize_approx=np.nan
cable.N_element=np.array(50)
cable.tempsupport=True
cable.N_tempsupport=np.array(11)
cable.polycoeff_hanger_adjust=np.nan

cable.NodeNumberBase=np.array([10e3,20e3])
cable.ElementNumberBase=np.array([10e3,20e3])

##########################
##########################
##########################

bridgedeck=struct()
bridgedeck.cs=struct()
bridgedeck.inertia=struct()
bridgedeck.gapbeam=struct()

bridgedeck.N_box=2

bridgedeck.cs.A=np.array([0.73,0.73])
bridgedeck.cs.I11=np.array([0.64,0.64])
bridgedeck.cs.I22=np.array([17.14,17.14])
bridgedeck.cs.I12=np.array([0,0])
bridgedeck.cs.It=np.array([1.85,1.85])
bridgedeck.cs.rho=np.array([0.0,0.0])
bridgedeck.cs.E=np.array([210e9,210e9])
bridgedeck.cs.G=np.array([81e9,81e9])
bridgedeck.cs.sc1=np.array([2.13,-2.13])
bridgedeck.cs.sc2=np.array([-0.20,-0.20])

bridgedeck.inertia.m=np.array([9300.0,9300.0])
bridgedeck.inertia.x1=np.array([0.0,0.0])
bridgedeck.inertia.x2=np.array([0.0,0.0])
bridgedeck.inertia.alpha=np.array([0.0,0.0])
bridgedeck.inertia.I11=np.array([6.4e4,6.4e4])
bridgedeck.inertia.I22=np.array([1.2e6,1.2e6])
bridgedeck.inertia.I12=np.array([0.0,0.0])

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
hanger.cs.rho=np.array(7850.0)
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
tower.cs.h_vec=np.array([14.5,10.5,8.5,8.5])
tower.cs.b_vec=np.array([12.5,9.5,8,8])
tower.cs.t_vec=np.array([1.5,1.5,1.5,1.5])
tower.cs.z_vec=np.array([30,75,75+316,400.0])
tower.cs.rho=np.array(2500.0)
tower.cs.E=np.array(35e9)
tower.cs.v=np.array(0.2)

tower.normaldir=np.array([0,1,0])
tower.eltype='B31'

tower.F_pullback_south=np.nan
tower.F_pullback_north=np.nan

tower.z_crossbeam_south=np.hstack((57.5-2-4,30+145.5+np.array([0.0,70.0,140.0,210.0])))
tower.z_crossbeam_north=tower.z_crossbeam_south

tower.h_crossbeam=np.array([8.0,8.0,8.0,8.0,8.0])
tower.b_crossbeam=np.array([5.0,5.0,5.0,5.0,5.0])
tower.t_crossbeam=np.array([1.0,1.0,1.0,1.0,1.0])

tower.N_element=np.nan
tower.meshsize=np.array(5.0)

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

geo.L_bridgedeck=np.array(2800.0)
geo.gap=np.array(29.974)

geo.dx_hanger=np.array(24.0)
geo.dx_endpiece_max=np.array(24.0)

geo.dx_pullback_south=np.array(-1)
geo.dx_pullback_north=np.array(1)

geo.z_cog_south=np.array(57.5)
geo.z_cog_north=np.array(57.5)
geo.z_cog_midspan=np.array(78.5)
geo.dz_cog_midspan_deflection=np.array(25)
geo.dz_cog_south_deflection=np.array(2.0)
geo.dz_cog_north_deflection=np.array(2.0)

geo.z_cable_top_south=np.array(400.0+0.1)
geo.z_cable_top_north=np.array(400.0+0.1)
geo.z_cable_midspan=np.array(81)
geo.dz_cable_deflection=np.array(30)

geo.dy_cable_anch_south=np.array(52.0)
geo.dy_cable_top_south=np.array(47.0)
geo.dy_cable_midspan=np.array(47.0)
geo.dy_cable_top_north=np.array(47.0)
geo.dy_cable_anch_north=np.array(52.0)

geo.dy_cog_hanger=np.array(8.0130)
geo.dz_cog_hanger=np.array(0.3324)
geo.dy_cog_inner=np.array(7.9870)
geo.dz_cog_inner=np.array(-0.5326)

geo.dy_pendulum=np.array(2.5)
geo.dz_slider=np.array(-1.5)
geo.dx_bearing_base=np.array(1.0)

geo.z_tower_base_south=np.array(30.0)
geo.z_tower_base_north=np.array(30.0)

geo.z_tower_top_south=np.array(400.0)
geo.z_tower_top_north=np.array(400.0)

geo.dy_tower_base_south=np.array(52.0)
geo.dy_tower_base_north=np.array(52.0)

geo.dy_tower_top_south=np.array(47.0)
geo.dy_tower_top_north=np.array(47.0)

geo.dx_tower_anch_south=np.array(718.5)
geo.dx_tower_anch_north=np.array(558.15)

geo.z_anch_south=np.array(0)
geo.z_anch_north=np.array(200.6)

geo.x_tower_south=np.array(-1400.0)
geo.x_tower_north=np.array(1400.0)