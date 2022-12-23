# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:35:26 2022

@author: oyvinpet
"""

#%%

import numpy as np
import scipy
from scipy import linalg
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.spatial.transform import Rotation as Rotation
import sys

import putools

#%%

def CalculateDisplacements(KT,P,ModelInfo):

    # Eliminate DOFs not used
    P_red=P[ModelInfo.IndexInclude]
    # KT_red=KT[ModelInfo.IxInclude]
    # r_red=np.linalg.solve(KT_red,P_red)
    
    KT_sparse=sparse.csr_matrix(KT)
    KT_red=KT_sparse[ModelInfo.IxInclude]
    r_red=spsolve(KT_red,P_red)
    
    r=ModelInfo.S_red @ r_red
    
    return r,KT_red
#%%

def CoordinateTransform_old(e1,e2):
    
    # # This routine calculates the rotation matrix R that transforms a vector a
    # # from a cordinate system defined by the orthogonal base vectors E1,E2,E3
    # # to a coordinate system defined by the orthogonal vectors e1,e2 and e3 for
    # # reference see Kolbein Bell "Matrise Statikk"
    
    # Normalize
    e1=e1/putools.num.norm_fast(e1)
    e2=e2/putools.num.norm_fast(e2)

    # Crossproduct
    e3=putools.num.cross_fast(e1,e2)
    
    # T=np.vstack((e1.T,e2.T,e3.T))
    T=np.array([e1,e2,e3])
    
    return T

#%%    
def CoordinateTransform(e1,e2):
    
    # Normalize
    e1=e1/putools.num.norm_fast(e1)
    e2=e2/putools.num.norm_fast(e2)

    # Crossproduct
    e3=putools.num.cross_fast(e1,e2)
    
    # T=np.array([e1,e2,e3])
    
    return np.array([e1,e2,e3])

#%%
    
    
def CordinateTransfromInc(RT,e2,X1,X2,rA,rB,L):

    # Vector along deformed element
    e1=((X2+rB)-(X1+rA))/L
    
    # The e2 direction is the e2 rotated for each node, then averaged over the new e2 directions for these two nodes
    e2a=RT[:,:,0].dot(e2)
    e2b=RT[:,:,1].dot(e2)
    
    # e2ab=1*(e2a+e2b)
    
    e3=putools.num.cross_fast(e1,e2a+e2b)
    
    # e3=e3/putools.num.norm_fast(e3)
    e2=putools.num.cross_fast(e3,e1)
    
    # TC0n=CoordinateTransform(e1,e2)
    e2=e2/putools.num.norm_fast(e2)
    e3=putools.num.cross_fast(e1,e2)
    TC0n=np.array([e1,e2,e3])
    
    return TC0n

#%%

def DistLoadProjXY(ModelInfo,pz,index=''):

    if index=='':
        index=np.arange(ModelInfo.N_el)
        
    index=putools.num.ensurenp(index)

    P=np.zeros(ModelInfo.N_DOF)
    
    for k in index:
    
        TC0=ModelInfo.TC0[k]
    
        X1=ModelInfo.ElCoord_1[k]
        X2=ModelInfo.ElCoord_2[k]
    
        L0=putools.num.norm_fast(X2-X1)
    
        L0_xy=putools.num.norm_fast(X2[0:1]-X1[0:1])
    
        # angle with projection line in xy-plane
        alpha=np.arctan2(X2[2]-X1[2],L0_xy)

        q=pz*L0_xy/L0
    
        qn=q*np.cos(alpha)
        qt=q*np.sin(alpha)
    
        P_loc=L0/60*np.array([ 
        30*qt , 0 , 30*qn ,
        0 , -5*qn*L0 , 0 , 
        30*qt  ,  0 , 30*qn ,
        0 , 5*qn*L0 , 0])
    
        # TT=scipy.linalg.block_diag(TC0,TC0,TC0,TC0).T
        TT=putools.num.block_diag_rep(TC0,4).T

        P_glob=TT.dot(P_loc)
    
        Ind_DOF=np.hstack((ModelInfo.ElDofIndex_1[k],ModelInfo.ElDofIndex_2[k]))
        
        P_add=np.zeros(np.shape(P))
        P_add[Ind_DOF]=P_glob
        
        P=P+P_add
    
    return P
    
#%%

def ElementNormal(ElementMatrix,NodeMatrix):
    
    e2mat=np.zeros((np.shape(ElementMatrix)[0],4))*np.nan
    e3mat=np.zeros((np.shape(ElementMatrix)[0],4))*np.nan
    
    for k in np.arange(np.shape(ElementMatrix)[0]):
        
        Index1=ElementMatrix[k,1]
        Index2=ElementMatrix[k,2]

        X1=NodeMatrix[Index1,1:]
        X2=NodeMatrix[Index2,1:]
        
        e1=X2-X1
        e1=e1/putools.num.norm_fast(e1)
        e3_guess=np.array([0, 0 ,1])
        
        e2=putools.num.cross_fast(e3_guess,e1)
        e2=e2/putools.num.norm_fast(e2)
        
        e3=putools.num.cross_fast(e1,e2)
        e3=e3/putools.num.norm_fast(e3)
        
        e2mat[k,1:]=e2
        e3mat[k,1:]=e3
        
        e2mat[k,0]=ElementMatrix[k,0]
        e3mat[k,0]=ElementMatrix[k,0]
        
    return e2mat,e3mat

#%%

def ExRot(R):

    # Algorithm for rotation tensor to rotation vector
    # Following Eq (2.12) in Bruheim
    
    d1=0.5*(R[3-1,2-1]-R[2-1,3-1])
    d2=0.5*(R[1-1,3-1]-R[3-1,1-1])
    d3=0.5*(R[2-1,1-1]-R[1-1,2-1])
    
    theta=np.arcsin(np.sqrt(d1**2+d2**2+d3**2))
    
    # Set to factor when angle is small
    if np.abs(theta)<1e-12:
        factor=1; # Factor set 1 (not 0), bug fix
    else:
        factor=theta/np.sin(theta)
    
    d=np.array([d1,d2,d3])
    
    theta_vec=factor*d
    
    return theta_vec

#%% Not so fast

def ExRot_fast(R):

    d=0.5*np.array([R[3-1,2-1]-R[2-1,3-1],
                    R[1-1,3-1]-R[3-1,1-1],
                    R[2-1,1-1]-R[1-1,2-1]])
    
    theta=np.arcsin(putools.num.norm_fast(d))
    
    # Set to factor when angle is small
    if np.abs(theta)<1e-12:
        factor=1; # Factor set 1 (not 0), bug fix
    else:
        factor=theta/np.sin(theta)
    
    # theta_vec=factor*d
    
    return factor*d

#%%

def GravityLoad2(ModelInfo):

    P=np.zeros((ModelInfo.N_DOF))
 
    for k in np.arange(ModelInfo.N_el):
    
        ElTypeId=ModelInfo.ElementMatrix[k,3]
        
        ElTypeIdIndex=np.nonzero(ElTypeId==ModelInfo.ElTypeId)[0][0]
        
        A=ModelInfo.A[ElTypeIdIndex]
        rho=ModelInfo.rho[ElTypeIdIndex]
        TC0=ModelInfo.TC0[k]
    
        X1=ModelInfo.ElCoord_1[k]
        X2=ModelInfo.ElCoord_2[k]
    
        L0=putools.num.norm_fast(X2-X1)
    
        L0_xy=putools.num.norm_fast(X2[0:2]-X1[0:2])
    
        # angle with projection line in xy-plane
        alpha=np.arctan2(X2[3-1]-X1[3-1],L0_xy)
    
        g=9.81
        m=rho*A
        q=-m*g; # load in z-direction pr unit length along the element axis
    
        qn=q*np.cos(alpha) # normal to beam
        qt=q*np.sin(alpha) # tangential to beam
    
        P_loc=L0/60*np.array([ 
        30*qt , 0 , 30*qn ,
        0 , -5*qn*L0 , 0 , 
        30*qt  ,  0 , 30*qn ,
        0 , 5*qn*L0 , 0])
    
        # TT=scipy.linalg.block_diag(TC0,TC0,TC0,TC0).T
        TT=putools.num.block_diag_rep(TC0,4).T

        P_glob=TT.dot(P_loc)
    
        Ind_DOF=np.hstack((ModelInfo.ElDofIndex_1[k],ModelInfo.ElDofIndex_2[k]))
        
        P_add=np.zeros(np.shape(P))
        P_add[Ind_DOF]=P_glob;
        
        P=P+P_add

    return P

#%%

def IncrementalRotation_old(r,RT):

    RT_out=np.zeros(np.shape(RT))
    for n in np.arange(int(len(r)/6)):
        
        RotInc=np.zeros(3)
    
        RotInc[1-1]=r[6*(n+1)-2-1]
        RotInc[2-1]=r[6*(n+1)-1-1]
        RotInc[3-1]=r[6*(n+1)-1]
    
        R=RodriguesRotationFormula(RotInc)
    
        RT_out[:,:,n]=R @ RT[:,:,n]
    
    return RT_out

#%%

def IncrementalRotation(r,RT):
    
    R=np.zeros(np.shape(RT))
    for n in np.arange(int(len(r)/6)):
        R[:,:,n]=Rotation.from_rotvec(r[6*(n+1)-2-1:6*(n+1)]).as_matrix()
    
    RT_out=np.einsum('nmk,mjk->njk',R,RT)
    return RT_out

#%%

def RodriguesRotationFormula(theta_vec):
    
    # Implemented as Eq.(2.10) in Bruheim
    # See also https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    
    # Find scalar magnitude
    theta=putools.num.norm_fast(theta_vec)
    
    # If theta is almost zero, set R=I to avoid numerical 0/0 problems
    if theta<1e-10:
        R=np.eye(3)
    else:
        n_vec=theta_vec/theta
        
        # Spin matrix
        N=np.zeros((3,3))
        N[1-1,2-1]=-n_vec[3-1]
        N[1-1,3-1]=n_vec[2-1]
        N[2-1,3-1]=-n_vec[1-1]
        N=N-N.T
        
        R=np.eye(3)*np.cos(theta)+N*np.sin(theta)+(1-np.cos(theta))*np.outer(n_vec,n_vec)
        # if np.isnan(R).any():
            # print('***** ERROR RodriguesRotationFormula')
    
    return R

#%%

def K_el_matrix(r_sub,RT_sub,L0,A,Iz,Iy,It,E,G,X1,X2,e2,TC0):
    
    # Displacements in global coordinates
    
    rA=r_sub[0:3]
    rB=r_sub[6:9]
    # L0=putools.num.norm_fast((X2-X1))
    L=putools.num.norm_fast(((X2+rB)-(X1+rA)))
    DL=L-L0
    
    # Linear strain
    epsilon=DL/L
    
    N=1*E*A*epsilon # N positive as tension
    
    # Obtain the transformation matrix
    e1=(X2-X1)/L0
    
    # Transformasjon mellom initial (C0) og rotated (C0n) configuration in each node
    TC0n=CordinateTransfromInc(RT_sub,e2,X1,X2,rA,rB,L)
    
    # RTdef=np.zeros((3,3,2))
    RTdefA=TC0n @ RT_sub[:,:,0] @ TC0.T
    RTdefB=TC0n @ RT_sub[:,:,1] @ TC0.T
    
    # Calculate the bending deformation of the element in end A (Local coordinates)
    
    phi_a=ExRot_fast(RTdefA)
    phi_b=ExRot_fast(RTdefB)
    
    # Define the deformation vector and the axial force in the element
    
    # rdef=np.hstack((np.zeros((3)),phi_a,np.array([DL,0,0]),phi_b))
    rdef=np.concatenate((np.zeros((3)),phi_a,np.array([DL,0,0]),phi_b),axis=0)    
    
    # Obtain the stiffness matrix in local element coordinates
    
    #Material stiffness
    
    KK=np.array([
    [E*A/L       ,   0                ,   0                ,   0        ,   0                ,   0               , -E*A/L   ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0           ,   12*E*Iz/(L**3)   ,   0                ,   0        ,   0                ,   6*E*Iz/(L**2)   , 0        ,   -12*E*Iz/(L**3)  ,   0                 ,   0         ,   0                ,   6*E*Iz/(L**2)   ],
    [0           ,   0                ,   12*E*Iy/(L**3)   ,   0        ,   -6*E*Iy/(L**2)   ,   0               , 0        ,   0                ,   -12*E*Iy/(L**3)   ,   0         ,   -6*E*Iy/(L**2)   ,   0               ],
    [0           ,   0                ,   0                ,   G*It/L   ,   0                ,   0               , 0        ,   0                ,   0                 ,   -G*It/L   ,   0                ,   0               ],
    [0           ,   0                ,   -6*E*Iy/(L**2)   ,   0        ,   4*E*Iy/(L)       ,   0               , 0        ,   0                ,   6*E*Iy/(L**2)     ,   0         ,   2*E*Iy/(L)       ,   0               ],
    [0           ,   6*E*Iz/(L**2)    ,   0                ,   0        ,   0                ,   4*E*Iz/(L)      , 0        ,   -6*E*Iz/(L**2)    ,   0                ,   0         ,   0                ,   2*E*Iz/(L)      ],
    [-E*A/L   ,   0                ,   0                 ,   0         ,   0                ,   0                , E*A/L    ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   -12*E*Iz/(L**3)  ,   0                 ,   0         ,   0                ,   -6*E*Iz/(L**2)   , 0        ,   12*E*Iz/(L**3)   ,   0                 ,   0         ,   0                ,   -6*E*Iz/(L**2)  ],
    [0        ,   0                ,   -12*E*Iy/(L**3)   ,   0         ,   6*E*Iy/(L**2)    ,  0                 , 0        ,   0                ,   12*E*Iy/(L**3)    ,   0         ,   +6*E*Iy/(L**2)   ,   0               ],
    [0        ,   0                ,   0                 ,   -G*It/L   ,   0                ,   0                , 0        ,   0                ,   0                 ,   G*It/L    ,   0                ,   0               ],
    [0        ,   0                ,   -6*E*Iy/(L**2)    ,   0         ,   2*E*Iy/(L)       ,   0                , 0        ,   0                ,   +6*E*Iy/(L**2)    ,   0         ,   4*E*Iy/(L)       ,   0               ],
    [0        ,   6*E*Iz/(L**2)    ,   0                 ,   0         ,   0                ,   2*E*Iz/(L)       , 0        ,   -6*E*Iz/(L**2)   ,   0                 ,   0         ,   0                ,   4*E*Iz/(L)      ]
    ])
    
    
    KKG=np.array([
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ,   0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   6/5/L            ,   0                 ,   0         ,   0                ,   1/10            ,   0        ,   -6/5/L           ,   0                 ,   0         ,   0                ,   1/10            ],
    [0        ,   0                ,   6/5/L             ,   0         ,   -1/10            ,   0               ,   0        ,   0                ,   -6/5/L            ,   0         ,   -1/10            ,   0               ],
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ,   0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   0                ,   -1/10             ,   0         ,   2/15*L           ,   0               ,   0        ,   0                ,   1/10             ,   0         ,   -1/30*L          ,   0                ],
    [0        ,   1/10             ,   0                 ,   0         ,   0                ,   2/15*L          ,   0        ,   -1/10             ,   0                 ,   0         ,   0                ,   -1/30*L        ],
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ,   0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   -6/5/L           ,   0                 ,   0         ,   0                ,   -1/10           ,   0        ,   6/5/L            ,   0                 ,   0         ,   0                ,   -1/10           ],
    [0        ,   0                ,   -6/5/L            ,   0         ,   1/10            ,   0                ,   0        ,   0                ,   6/5/L             ,   0         ,   +1/10            ,   0               ],
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ,   0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   0                ,   -1/10             ,   0         ,   -1/30*L          ,   0               ,   0        ,   0                ,   +1/10             ,   0         ,   2/15*L           ,   0               ],
    [0        ,   1/10             ,   0                 ,   0         ,   0                ,   -1/30*L         ,   0        ,   -1/10            ,   0                 ,   0         ,   0                ,   2/15*L          ]
    ])    
 
    # Add geometric and material stiffness
    K_el=KK+N*KKG
    
    #  Calculate the residual and the stiffness matrix in global coordinates
    TT1=putools.num.block_diag_rep(TC0n,4)

    RHS=TT1.T @ K_el @ rdef
    RHSsub1=RHS[0:6]
    RHSsub2=RHS[6:12]
    
    # TT2=scipy.linalg.block_diag(TC0n,TC0n)
    TT2=TT1
    
    KK_elGlob=TT2.T @ K_el @ TT2
    
    # if np.any(np.abs(K_el-K_el.T)/np.linalg.norm(K_el) > 1e-6):
        # raise Exception('Local stiffness matrix not symmetric')
    
    return (RHSsub1, RHSsub2, KK_elGlob,N)


#%%

def K_el_matrix_old(r_sub,RT_sub,A,Iz,Iy,It,E,G,X1,X2,e2,TC0):
    
    # Displacements in global coordinates
    
    rA=r_sub[0:3]
    rB=r_sub[6:9]
    L0=putools.num.norm_fast((X2-X1))
    L=putools.num.norm_fast(((X2+rB)-(X1+rA)))
    DL=L-L0
    
    # Linear strain
    epsilon=DL/L
    
    N=1*E*A*epsilon # N positive as tension
    
    # Obtain the transformation matrix
    e1=(X2-X1)/L0
    
    # Transformation matrix between global coordinates to initial (C0) configuration
    # if np.isnan(TC0).any(): # TC0 can be supplied as an input, skipping repeated calculations
        # TC0=CoordinateTransform(e1,e2)
    
    # Transformasjon mellom initial (C0) og rotated (C0n) configuration in each node
    TC0n=CordinateTransfromInc(RT_sub,e2,X1,X2,rA,rB,L)
    
    # RTdef=np.zeros((3,3,2))
    RTdefA=TC0n @ RT_sub[:,:,0] @ TC0.T
    RTdefB=TC0n @ RT_sub[:,:,1] @ TC0.T
    
    # Calculate the bending deformation of the element in end A (Local coordinates)
    
    phi_a=ExRot_fast(RTdefA)
    phi_b=ExRot_fast(RTdefB)
    
    # Define the deformation vector and the axial force in the element
    
    # rdef=np.hstack((np.zeros((3)),phi_a,np.array([DL,0,0]),phi_b))
    rdef=np.concatenate((np.zeros((3)),phi_a,np.array([DL,0,0]),phi_b),axis=0)    
    
    # Obtain the stiffness matrix in local element coordinates
    
    #Material stiffness
    # KKsub11=np.zeros((6,6))
    # KKsub12=np.zeros((6,6))
    # KKsub22=np.zeros((6,6))
    #------------------------%
    
    KKsub11=np.array([
    [E*A/L       ,   0                ,   0                ,   0        ,   0                ,   0               ],
    [0           ,   12*E*Iz/(L**3)   ,   0                ,   0        ,   0                ,   6*E*Iz/(L**2)   ],
    [0           ,   0                ,   12*E*Iy/(L**3)   ,   0        ,   -6*E*Iy/(L**2)   ,   0               ],
    [0           ,   0                ,   0                ,   G*It/L   ,   0                ,   0               ],
    [0           ,   0                ,   -6*E*Iy/(L**2)   ,   0        ,   4*E*Iy/(L)       ,   0               ],
    [0           ,   6*E*Iz/(L**2)    ,   0                ,   0        ,   0                ,   4*E*Iz/(L)      ]
    ])
    
    # KKsub11[2-1,6-1]=6*E*Iz/(L**2)
    # KKsub11[3-1,5-1]=-6*E*Iy/(L**2)
    # KKsub11=KKsub11+KKsub11.T
    # KKsub11[1-1,1-1]=E*A/L
    # KKsub11[2-1,2-1]=12*E*Iz/(L**3)
    # KKsub11[3-1,3-1]=12*E*Iy/(L**3)
    # KKsub11[4-1,4-1]=G*It/L
    # KKsub11[5-1,5-1]=4*E*Iy/(L)
    # KKsub11[6-1,6-1]=4*E*Iz/(L)
    #------------------------%
    
    
    KKsub12=np.array([
    [-E*A/L   ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   -12*E*Iz/(L**3)  ,   0                 ,   0         ,   0                ,   6*E*Iz/(L**2)   ],
    [0        ,   0                ,   -12*E*Iy/(L**3)   ,   0         ,   -6*E*Iy/(L**2)   ,   0               ],
    [0        ,   0                ,   0                 ,   -G*It/L   ,   0                ,   0               ],
    [0        ,   0                ,   6*E*Iy/(L**2)    ,   0         ,   2*E*Iy/(L)       ,   0               ],
    [0        ,   -6*E*Iz/(L**2)    ,   0                 ,   0         ,   0                ,   2*E*Iz/(L)      ]
    ])
    
    
    # KKsub12[2-1,6-1]=6*E*Iz/(L**2)
    # KKsub12[3-1,5-1]=-6*E*Iy/(L**2)
    # KKsub12=KKsub12-KKsub12.T
    # KKsub12[1-1,1-1]=-E*A/L
    # KKsub12[2-1,2-1]=-12*E*Iz/(L**3)
    # KKsub12[3-1,3-1]=-12*E*Iy/(L**3)
    # KKsub12[4-1,4-1]=-G*It/L
    # KKsub12[5-1,5-1]=2*E*Iy/(L)
    # KKsub12[6-1,6-1]=2*E*Iz/(L)
    #------------------------%
    KKsub21=KKsub12.T
    #------------------------%
        
    KKsub22=np.array([
    [E*A/L    ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   12*E*Iz/(L**3)   ,   0                 ,   0         ,   0                ,   -6*E*Iz/(L**2)  ],
    [0        ,   0                ,   12*E*Iy/(L**3)    ,   0         ,   +6*E*Iy/(L**2)   ,   0               ],
    [0        ,   0                ,   0                 ,   G*It/L    ,   0                ,   0               ],
    [0        ,   0                ,   +6*E*Iy/(L**2)    ,   0         ,   4*E*Iy/(L)       ,   0               ],
    [0        ,   -6*E*Iz/(L**2)   ,   0                 ,   0         ,   0                ,   4*E*Iz/(L)      ]
    ])
    
    # KKsub22[2-1,6-1]=-6*E*Iz/(L**2)
    # KKsub22[3-1,5-1]=+6*E*Iy/(L**2)
    # KKsub22=KKsub22+KKsub22.T
    # KKsub22[1-1,1-1]=E*A/L
    # KKsub22[2-1,2-1]=12*E*Iz/(L**3)
    # KKsub22[3-1,3-1]=12*E*Iy/(L**3)
    # KKsub22[4-1,4-1]=G*It/L
    # KKsub22[5-1,5-1]=4*E*Iy/(L)
    # KKsub22[6-1,6-1]=4*E*Iz/(L)
    #------------------------%
    # Geometric stiffness
    # KKGsub11=np.zeros((6,6))
    # KKGsub12=np.zeros((6,6))
    # KKGsub22=np.zeros((6,6))
    #------------------------%
    
    KKGsub11=np.array([
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   6/5/L            ,   0                 ,   0         ,   0                ,   1/10            ],
    [0        ,   0                ,   6/5/L             ,   0         ,   -1/10            ,   0               ],
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   0                ,   -1/10             ,   0         ,   2/15*L           ,   0               ],
    [0        ,   1/10             ,   0                 ,   0         ,   0                ,   2/15*L          ]
    ])
    
    # KKGsub11[2-1,6-1]=1/10
    # KKGsub11[3-1,5-1]=-1/10
    # KKGsub11=KKGsub11+KKGsub11.T
    # KKGsub11[2-1,2-1]=6/5/L
    # KKGsub11[3-1,3-1]=6/5/L
    # KKGsub11[5-1,5-1]=2/15*L
    # KKGsub11[6-1,6-1]=2/15*L
    #------------------------%
    
    KKGsub12=np.array([
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   -6/5/L           ,   0                 ,   0         ,   0                ,   1/10            ],
    [0        ,   0                ,   -6/5/L            ,   0         ,   -1/10            ,   0               ],
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   0                ,   1/10             ,   0         ,   -1/30*L          ,   0                ],
    [0        ,   -1/10             ,   0                 ,   0         ,   0                ,   -1/30*L        ]
    ])
    

    # KKGsub12[2-1,6-1]=1/10
    # KKGsub12[3-1,5-1]=-1/10
    # KKGsub12=KKGsub12-KKGsub12.T
    
    # KKGsub12[2-1,2-1]=-6/5/L
    # KKGsub12[3-1,3-1]=-6/5/L
    # KKGsub12[5-1,5-1]=-1/30*L
    # KKGsub12[6-1,6-1]=-1/30*L
    #------------------------%
    KKGsub21=KKGsub12.T
    #------------------------%
    KKGsub22=np.array([
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   6/5/L            ,   0                 ,   0         ,   0                ,   -1/10           ],
    [0        ,   0                ,   6/5/L             ,   0         ,   +1/10            ,   0               ],
    [0        ,   0                ,   0                 ,   0         ,   0                ,   0               ],
    [0        ,   0                ,   +1/10             ,   0         ,   2/15*L           ,   0               ],
    [0        ,   -1/10            ,   0                 ,   0         ,   0                ,   2/15*L          ]
    ])
    
    
    # KKGsub22[2-1,6-1]=-1/10
    # KKGsub22[3-1,5-1]=+1/10;
    # KKGsub22=KKGsub22+KKGsub22.T
    # KKGsub22[2-1,2-1]=6/5/L
    # KKGsub22[3-1,3-1]=6/5/L
    # KKGsub22[5-1,5-1]=2/15*L
    # KKGsub22[6-1,6-1]=2/15*L
    #------------------------%
    
    # Add geometric and material stiffness
    KKsub11=KKsub11  +N*KKGsub11     
    KKsub12=KKsub12  +N*KKGsub12    
    KKsub21=KKsub21  +N*KKGsub21     
    KKsub22=KKsub22  +N*KKGsub22
    
    #  Calculate the residual and the stiffness matrix in global coordinates
    # TT1=scipy.linalg.block_diag(TC0n,TC0n,TC0n,TC0n)
    TT1=putools.num.block_diag_rep(TC0n,4)

    K_el=np.concatenate( (np.concatenate((KKsub11,KKsub12),axis=1),np.concatenate((KKsub21,KKsub22),axis=1)),axis=0)


    RHS=TT1.T @ K_el @ rdef
    RHSsub1=RHS[0:6]
    RHSsub2=RHS[6:12]
    
    # TT2=scipy.linalg.block_diag(TC0n,TC0n)
    TT2=TT1[0:6,0:6]

    KKsubGlob11=(TT2.T @ KKsub11 @ TT2)
    KKsubGlob12=(TT2.T @ KKsub12 @ TT2)
    KKsubGlob21=(TT2.T @ KKsub21 @ TT2)
    KKsubGlob22=(TT2.T @ KKsub22 @ TT2)
    
    # if np.any(np.abs(K_el-K_el.T)/np.linalg.norm(K_el) > 1e-6):
        # raise Exception('Local stiffness matrix not symmetric')
    
    return (RHSsub1, RHSsub2, KKsubGlob11, KKsubGlob12, KKsubGlob21, KKsubGlob22,N)
    
    
