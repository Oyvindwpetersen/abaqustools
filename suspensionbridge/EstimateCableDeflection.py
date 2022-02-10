function [cable,geo,tower]=EstimateCableDeflectionMain(cable,bridgedeck,hanger,tower,bearing,sadle,geo)

#%% 

# clc
# clear all
# close all
# 
# UserParameterFileName=['C:\Cloud\OD_OWP\Work\Abaqus\Suspensionbridge\LangenuenModel\UserParametersLangenuen.m']
# 
# [cable,bridgedeck,hanger,tower,bearing,sadle,geo,abaqus,modal]=ProcessUserParameters(UserParameterFileName);

#%%  Iterate
# 
# scalefactor_cable=1;
# scalefactor_bridgedeck=1;

r_u3_mid_initial=geo.dz_cable_deflection;
r_u1_top_south_initial=geo.dx_pullback_south;
r_u1_top_north_initial=geo.dx_pullback_north;

for iter=1:3

    EstimateCableDeflectionSub;
    
    r_u1_top=r{2}(IndexTop_U1);
    geo.dx_pullback_south=-r_u1_top[1]
    geo.dx_pullback_north=-r_u1_top[2]

    r_u3_mid=abs(r{2}(IndexMid_U3));
    geo.dz_cable_deflection=r_u3_mid;

    r_u1_top_all(:,iter)=r_u1_top;
    r_u3_mid_all(iter)=r_u3_mid;
    
    if ~isempty(cable.cs.sigma_target)
    cable.cs.A=max(N)/(cable.cs.sigma_target);
    end
    
end

numtools.starprint({['Initialized dz_cable_deflection=' + num2str(r_u3_mid_initial,'%0.3f') ' m'] ['Iterated dz_cable_deflection=' + num2str(r_u3_mid,'%0.3f') ' m']},1);

#%%  Displacement in x-dir

r_u1_hanger=r{2}(IndexMainspan_U1).';

x_hat=meta.x_hanger./(geo.L_bridgedeck/2);
polycoeff=np.polyfit(x_hat,r_u1_hanger,3);
polycoeff=round(polycoeff,3);

cable.polycoeff_hanger_adjust=polycoeff;

#%%  Tower 

geo.dx_pullback_south=-r_u1_top_all(1,end);
geo.dx_pullback_north=-r_u1_top_all(2,end);

tower.F_pullback_south=geo.dx_pullback_south*tower.K_south;
tower.F_pullback_north=geo.dx_pullback_north*tower.K_north;

numtools.starprint({['Initialized dx_pullback_south=' + num2str(r_u1_top_south_initial,'%0.3f') ' m'] ['Iterated dx_pullback_south=' + num2str(geo.dx_pullback_south,'%0.3f') ' m']},1);
numtools.starprint({['Initialized dx_pullback_north=' + num2str(r_u1_top_north_initial,'%0.3f') ' m'] ['Iterated dx_pullback_north=' + num2str(geo.dx_pullback_north,'%0.3f') ' m']},1);

#%%  Displacement under cable load only

# scalefactor_cable=1;
# scalefactor_bridgedeck=0;
# 
# EstimateCableDeflectionSub;

r_u3_temp2=abs(r{1}(IndexMid_U3));

dz_cog_midspan_deflection_temp=geo.dz_cog_midspan_deflection;

geo.dz_cog_midspan_deflection=r_u3_mid-r_u3_temp2;

numtools.starprint({['Initialized dz_cog_midspan_deflection=' + num2str(dz_cog_midspan_deflection_temp,'%0.3f') ' m'] ['Iterated dz_cog_midspan_deflection=' + num2str(geo.dz_cog_midspan_deflection,'%0.3f') ' m']},1);



#%% 
# clc

meta=struct();

[meta,cablemesh_temp]=CableGeometry([],meta,geo,cable);

NodeMatrix=stackVertical(cablemesh_temp.NodeMatrix);

ElementMatrix=stackVertical(cablemesh_temp.ElementMatrix);

ElementType(ElementMatrix(:,1)<500e3,1)=2;
ElementType(ElementMatrix(:,1)>500e3,1)=10;

ElementMatrix=[ElementMatrix ElementType]

[e2mat,e3mat]=ElementNormal(ElementMatrix,NodeMatrix);

ModelInfo.NodeMatrix=NodeMatrix;
ModelInfo.ElementMatrix=ElementMatrix;

ModelInfo.e2mat=e2mat;

ModelInfo.A=[ cable.cs.A 1]
ModelInfo.Iz=[ cable.cs.I11 1]
ModelInfo.Iy=[ cable.cs.I22 1]
ModelInfo.It=[ cable.cs.It 1]
ModelInfo.E=[ cable.cs.E 210e9]
ModelInfo.G=[ cable.cs.G 80e9]
ModelInfo.rho=[ cable.cs.rho 0]

#%% 

NodeNoAnch=cablemesh_temp.NodeSet{getCellIndex('Cable_main_anchorage',cablemesh_temp.NodeSetName)};
NodeSetNameTop=['Cable_main_top_south_west' , 'Cable_main_top_north_west' , 'Cable_main_top_south_east' , 'Cable_main_top_north_east']
NodeNoTop=[]
for k=1:4
    IndexTop_U1=getCellIndex(NodeSetNameTop{k},cablemesh_temp.NodeSetName);
    NodeNoTop=[NodeNoTop cablemesh_temp.NodeSet{IndexTop_U1}]
end

#%% 

ModelInfo.DofLabel=getLabel('all',[ModelInfo.NodeMatrix(:,1)])
ModelInfo.DofExclude=mergecell(getLabel({'U1' , 'U2' , 'U3'],[NodeNoAnch]),getLabel({ 'U2' , 'U3' },[NodeNoTop]));

ModelInfo=ProcessModel(ModelInfo);

#%%  

NodeIndCable1=find(ModelInfo.NodeMatrix(:,1)<20e3);
NodeNoCable1=ModelInfo.NodeMatrix(NodeIndCable1,1);

NodeIndCable2=find(ModelInfo.NodeMatrix(:,1)>20e3 and ModelInfo.NodeMatrix(:,1)<500e3);
NodeNoCable2=ModelInfo.NodeMatrix(NodeIndCable2,1);

[~,ind_min]=min(abs(ModelInfo.NodeMatrix(NodeIndCable1,2)));
NodeIndCableMid1=NodeIndCable1(ind_min);
NodeNoCableMid1=NodeNoCable1(NodeIndCableMid1);

IndexMid_U3=getCellIndex(getLabel('U3',NodeNoCableMid1),ModelInfo.DofLabel);

NodeNumberMainSpan1=NodeNoTop[1]:NodeNoTop[2] NodeNumberMainSpan1=NodeNumberMainSpan1(2:end-1);
IndexMainspan_U1=getCellIndex(getLabel('U1',NodeNumberMainSpan1),ModelInfo.DofLabel);

#%%  Tower force

IndexTop_U1=getCellIndex(getLabel('U1',NodeNoTop),ModelInfo.DofLabel);

Sp_u1=sparse(1:4,IndexTop_U1,ones(1,4),4,ModelInfo.N_DOF);
r_pre=[geo.dx_pullback_south geo.dx_pullback_north geo.dx_pullback_south geo.dx_pullback_north]';

# K_tower=7.284e+05;
K_tower2=[tower.K_south;tower.K_north;tower.K_south;tower.K_north]

# TowerForceFunction=@(r) Sp_u1'*(K_tower.*(-Sp_u1*r-r_pre)); %+Sp2'*(-Sp2*r)*Ktow_z*0
TowerForceFunction=@(r) Sp_u1'*(K_tower2.*(-Sp_u1*r-r_pre)); %+Sp2'*(-Sp2*r)*Ktow_z*0

#%% 

# P_cable=GravityLoad(ModelInfo);
P_cable=GravityLoad2(ModelInfo);

# Load for both bridgedecks (if two) 
pz=-sum(bridgedeck.inertia.m*9.81);

IndexLoad=[]
for k=1:ModelInfo.N_el

    if ~any(floor(ModelInfo.ElementMatrix(k,1)/1e3)==[10 20]) continue; end
    if  abs( (ModelInfo.ElCoord{k}{1}[1]+ModelInfo.ElCoord{k}{2}[1])/2 )<geo.L_bridgedeck/2
    IndexLoad(end+1)=k;
    end
    
end

P_bridgedeck=DistLoadProjXY(ModelInfo,pz/2,IndexLoad);

P_loadstep{1}=P_cable;
P_loadstep{2}=P_cable+P_bridgedeck;


#%% 

# clc
close all

solveopt=struct();
solveopt.IncrementType='exp';
solveopt.LoadIncrements=6;
solveopt.PlotDef=false;
solveopt.PlotInterval=Inf;
solveopt.PlotNorm=false;
solveopt.NonLinearForce=TowerForceFunction;
# solveopt.LinearStiffness=LinearStiffness;
solveopt.norm_tol=1e-10;
solveopt.IterationMax=100;

[r,KT,K_add,RHS,R_NL,N]=NonLinearSolver(ModelInfo,P_loadstep,solveopt);



#%% 

%# 
# figure(); hold on;
# stem(getSubsetRow(r,getLabel('U1',NodeNoCable1),ModelInfo.DofLabel));
# stem(getSubsetRow(r,getLabel('U3',NodeNoCable1),ModelInfo.DofLabel));
# stem(getSubsetRow(r,getLabel('U2',NodeNoCable1),ModelInfo.DofLabel));
%
# KT*r





