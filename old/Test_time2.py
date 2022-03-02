# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 17:07:27 2022

@author: oyvinpet
"""
#%%

import numtools

import numpy as np


#%%

ind=[]
for k in range(100):
    
    ind.append(np.ix_(k*6+np.arange(6),k*6+np.arange(6)))


t0=numtools.tic()

for n in range(1000):
  
    
    A=np.zeros((1000,1000))
    
    for k in range(100):
    
        # K_el=[1,0,0,0,0,0  , 1,0,0,0,0,0  , 1,0,0,0,0,0  , 1,0,0,0,10,0  , 1,0,0,0,0,100  , 1,0,0,0,0,200  ]
        # A[ind[k]]=np.array(K_el).reshape((6,6))
        
        
        K_el=np.array( [ [1,0,0,0,0,0]  , [1,0,0,0,0,0]  , [1,0,0,0,0,0]  , [1,0,0,0,10,0]  , [1,0,0,0,0,100]  , [1,0,0,0,0,200]  ])
        A[ind[k]]=K_el
        
        
numtools.toc(t0)


#%%

from scipy.spatial.transform import Rotation as Rotation


RT=np.zeros((3,3,100))
r=np.random.randn(100*6)

t0=numtools.tic()
for k in range(50):
    R=np.zeros(np.shape(RT))
    for n in np.arange(int(len(r)/6)):
        R[:,:,n]=Rotation.from_rotvec(r[6*(n+1)-2-1:6*(n+1)]).as_matrix()
    # RT_out=np.einsum('nmk,mjk->njk',R,RT)
numtools.toc(t0)




A=np.random.randn(100,3)
t0=numtools.tic()
for k in range(50):
    
    R2=Rotation.from_rotvec(A).as_matrix()
    
    # RT_out2=np.einsum('nmk,mjk->njk',R,RT)
numtools.toc(t0)





# t0=numtools.tic()
# for k in range(1000):
#     R3=[Rotation.from_rotvec(r[6*(n+1)-2-1:6*(n+1)]).as_matrix() for  n in np.arange(int(len(r)/6))]
#     RT_out=np.einsum('nmk,mjk->njk',R,RT)
# numtools.toc(t0)



#%%
(KKsub11,KKsub12,KKsub21,KKsub22)=np.eye(6),np.eye(6),np.eye(6),np.eye(6)
TT2=np.eye(6)+2


t0=numtools.tic()
for k in range(106*6*8):
    # KKsubGlob11=(TT2.T @ KKsub11 @ TT2)
    # KKsubGlob12=(TT2.T @ KKsub12 @ TT2)
    # KKsubGlob21=(TT2.T @ KKsub21 @ TT2)
    # KKsubGlob22=(TT2.T @ KKsub22 @ TT2)
    K_el=np.concatenate( (np.concatenate((KKsub11,KKsub12),axis=1),np.concatenate((KKsub21,KKsub22),axis=1)),axis=0)

numtools.toc(t0)

#%%

import Corot
R=np.eye(3)/10
    
t0=numtools.tic()
for k in range(106*6*8*2):
    ExRot_fast(R)
numtools.toc(t0)

t0=numtools.tic()
for k in range(106*6*8*2):
    ExRot(R)
numtools.toc(t0)
    

#%%

t0=numtools.tic()
for k in range(6*8*2):
    for k in np.arange(200):
        
        # Index of all DOFs to DOFs in nodes
        n=ModelInfo.ElDofIndex[k][0]
        m=ModelInfo.ElDofIndex[k][1]
        
numtools.toc(t0)

ElDofIndex=[None]*200
for k in np.arange(200):
    ElDofIndex[k]=np.random.randn(1,6)

t0=numtools.tic()
for k in range(6*8*2):
    for k in np.arange(200):
        
        # Index of all DOFs to DOFs in nodes
        n=ElDofIndex[k]
        m=ElDofIndex[k]
        
numtools.toc(t0)

#%%

t0=numtools.tic()
for k in range(6*8*2):
    for k in np.arange(200):
        A=ModelInfo.A[0]
        # E=ModelInfo.E[0]
        
numtools.toc(t0)

t0=numtools.tic()
for k in range(6*8*2):
    A_list=ModelInfo.A
    # E_list=ModelInfo.E
    for k in np.arange(200):
        
        A=A_list[0]
        # E=E_list[0]
numtools.toc(t0)



#%%

r=np.random.randn(100)

n=[3,4,5]
m=[30,40,50]

n_m=n+m

t0=numtools.tic()
for k in range(int(1e6)):
    r_sub=r[n+m]
numtools.toc(t0)

t0=numtools.tic()
for k in range(int(1e6)):
    r_sub=r[n_m]
numtools.toc(t0)


#%%


t0=numtools.tic()
for k in range(int(1e6)):
    r_red=np.linalg.solve(KT_red,P_red)
numtools.toc(t0)


#%%

KT_full=KT_red

KT_sparse=sparse.csr_matrix(KT_red)

t0=numtools.tic()
for k in range(int(100)):
    r_red=np.linalg.solve(KT_red,P_red)
numtools.toc(t0)

t0=numtools.tic()
for k in range(int(100)):
    KT_sparse=sparse.csr_matrix(KT_red)
    r_red2=spsolve(KT_sparse,P_red)
numtools.toc(t0)




t0=numtools.tic()
for k in range(int(100)):
    KT_sparse=sparse.csr_matrix(KT)
    KT_red=KT_sparse[ModelInfo.IxInclude]
numtools.toc(t0)



t0=numtools.tic()
for k in range(int(100)):
    KT_red=KT[ModelInfo.IxInclude]
    KT_sparse=sparse.csr_matrix(KT_red)
numtools.toc(t0)





t0=numtools.tic()
for k in range(int(100)):
    KT_red=np.copy(KT)
    KT_red=np.delete(KT_red,ModelInfo.IndexExclude,axis=0)
    KT_red=np.delete(KT_red,ModelInfo.IndexExclude,axis=1)
numtools.toc(t0)



#%%
t00=numtools.tic()
for kkk in range(6*8):
    

    # t00=numtools.tic()
    N_nodes=np.shape(ModelInfo.NodeMatrix)[0]
    N_NodeDof=6
    N_el=np.shape(ModelInfo.ElementMatrix)[0]
    
    K=np.zeros((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    #K=sparse.dok_matrix((N_NodeDof*N_nodes,N_NodeDof*N_nodes))
    
    RHS=np.zeros(N_NodeDof*N_nodes)
    N=np.zeros(N_el)
    
    e2_mat_all=ModelInfo.e2mat
    
    TypeElIndex2_all=ModelInfo.TypeElIndex2
    
    A_all=ModelInfo.A
    Iz_all=ModelInfo.Iz
    Iy_all=ModelInfo.Iy
    It_all=ModelInfo.It
    E_all=ModelInfo.E
    G_all=ModelInfo.G
    TC0_all=ModelInfo.TC0

    NodeIndex_all=ModelInfo.NodeIndex

    ElDofIndex_1_all=ModelInfo.ElDofIndex_1
    ElDofIndex_2_all=ModelInfo.ElDofIndex_2
    
    ElCoord_1_all=ModelInfo.ElCoord_1
    ElCoord_2_all=ModelInfo.ElCoord_2
    
    K_idx_all=ModelInfo.K_idx
    
    
    for k in np.arange(N_el):
        
        # Index of all DOFs to DOFs in nodes
        # n=ElDofIndex_1_all[k]
        # m=ElDofIndex_2_all[k]
        
        # Initial coordinates of nodes
        # X1=ElCoord_1_all[k]
        # X2=ElCoord_2_all[k]
        # 
        # Lateral vector
        # e2=e2_mat_all[k,1:]
        
        # Cross sectional properties
        # ElTypeIndex=TypeElIndex2_all[k]
        
        # A=A_all[ElTypeIndex]
        # Iz=Iz_all[ElTypeIndex]
        # Iy=Iy_all[ElTypeIndex]
        # It=It_all[ElTypeIndex]
        # E=E_all[ElTypeIndex]
        # G=G_all[ElTypeIndex]
        # TC0=TC0_all[k]
        
        # NodeIndex=[ModelInfo.ElementMatrix[k,1],ModelInfo.ElementMatrix[k,2]]
        
        # NodeIndex=NodeIndex_all[k]
        r_sub=r[n+m]
        rA=r[n[0:3]]
        rB=r[m[0:3]]
        # RT_sub=RT[:,:,NodeIndex_all[k]]
        
        # Get matrix
        # t00=numtools.tic()
        # (RHSsub1,RHSsub2,K_el_sub11,K_el_sub12,K_el_sub21,K_el_sub22,N[k])=K_el_matrix(r_sub,RT_sub,A,Iz,Iy,It,E,G,X1,X2,e2,TC0)
        # numtools.toc(t00)
        
        # Assign to global stiffness matrix  
        # K_el=np.concatenate( (np.concatenate((K_el_sub11,K_el_sub12),axis=1),np.concatenate((K_el_sub21,K_el_sub22),axis=1)),axis=0)
        # K[K_idx_all[k]] += K_el
        
        # Axial force
        # N[k]=Nx_el;
        
        # RHS
        # RHS[n]+=RHSsub1
        # RHS[m]+=RHSsub2
        
numtools.toc(t00)


