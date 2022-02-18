# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:35:26 2022

@author: oyvinpet
"""



import numpy as np

#%%


    # Eliminate DOFs not used
    KT_red=KT[ModelInfo.IndexInclude,ModelInfo.IndexInclude]
    P_red=P[ModelInfo.IndexInclude]
    
    #  Solve
    r_red=np.linalg.solve(KT_red,P_red)
    
    r=ModelInfo.S_red @ r_red
    
    return r,KT_red
#%%

def CoordinateTransform(e1,e2):
    
    # # This routine calculates the rotation matrix R that transforms a vector a
    # # from a cordinate system defined by the orthogonal base vectors E1,E2,E3
    # # to a coordinate system defined by the orthogonal vectors e1,e2 and e3 for
    # # reference see Kolbein Bell "Matrise Statikk"
    
    # Normalize
    e1=e1/np.linalg.norm(e1)
    e2=e2/np.linalg.norm(e2)

    # Crossproduct
    e3=np.cross(e1,e2)
    
    T=np.vstack((e1.T,e2.T,e3.T))
    return T

     # Check orthogonality
    
    # if abs(dot(e1,e2))>1.0e-10
    #    beep
    #    warning('Unit vectors e1 and e2 are not orthogonal' )
    #    warning(['The dot product is ' num2str(dot(e1,e2)) ])
    #    return
    # end
    
    # if abs(dot(e1,e3))>1.0e-10
    #     beep
    #    warning('Unit vectors e1 and e3 are not orthogonal' )
    #    warning(['The dot product is ' num2str(dot(e1,e3)) ])
    #    return
    # end
    
    # if abs(dot(e2,e3))>1.0e-10
    #     beep
    #    warning('Unit vectors e2 and e3 are not orthogonal' )
    #    warning(['The dot product is ' num2str(dot(e1,e3)) ])
    #    return
    
    # end
    
    #%%
    
def CordinateTransfromInc(RT,e2,X1,X2,rA,rB,L):

    # Vector along deformed element
    e1=((X2+rB)-(X1+rA))/L
    
    # The e2 direction is the e2 rotated for each node, then averaged over the new e2 directions for these two nodes
    e2a=RT[:,:,0].dot(e2)
    e2b=RT[:,:,1].dot(e2)
    
    e2ab=1*(e2a+e2b)
    
    e3=np.cross(e1,e2ab)
    
    e3=e3/np.linalg.norm(e3)
    e2=np.cross(e3,e1)
    
    TC0n=CoordinateTransform(e1,e2)
    
    return TC0n
    
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
        e1=e1/np.linalg.norm(e1)
        e3_guess=np.array([0, 0 ,1])
        
        e2=np.cross(e3_guess,e1)
        e2=e2/np.linalg.norm(e2)
        
        e3=np.cross(e1,e2)
        e3=e3/np.linalg.norm(e3)
        
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

#%%

def GravityLoad2(ModelInfo):

    P=np.zeros((ModelInfo.N_DOF))
 
    for k in np.arange(ModelInfo.N_el):
    
        ElTypeId=ModelInfo.ElementMatrix[k,3]
        
        ElTypeIdIndex=np.nonzero(ElTypeId==ModelInfo.ElTypeId)[0]
        
        A=ModelInfo.A[ElTypeIdIndex]
        rho=ModelInfo.rho[ElTypeIdIndex]
        TC0=ModelInfo.TC0[k]
    
        X1=ModelInfo.ElCoord[k][0]
        X2=ModelInfo.ElCoord[k][1]
    
        L0=np.linalg.norm(X2-X1)
    
        L0_xy=np.linalg.norm(X2[0:2]-X1[0:2])
    
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
    
        TT=scipy.linalg.block_diag(TC0,TC0,TC0,TC0).T
        
        P_glob= TT.dot(P)
    
        Ind_DOF=np.hstack((ModelInfo.ElDofIndex[k][0],ModelInfo.ElDofIndex[k][1]))
        
        P_add=np.zeros(np.shape(P))
        P_add[Ind_DOF]=P_glob;
        
        P=P+P_add;

    return P

#%%

def IncrementalRotation(r,RT):

    for n in np.arange(np.shape(r,0)/6):
        
        RotInc=np.zeros(3,1)
    
        RotInc[1-1]=r[6*n-2-1,1-1]
        RotInc[2-1]=r[6*n-1-1,1-1]
        RotInc[3-1]=r[6*n-1,1-1]
    
        R=RodriguesRotationFormula(RotInc)
    
        RT[:,:,n]=R @ RT[:,:,n]
    
    return RT

#%%

def RodriguesRotationFormula(theta_vec):

    # Implemented as Eq.(2.10) in Bruheim
    # See also https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    
    # Find scalar magnitude
    theta=np.linalg.norm(theta_vec)
    
    # If theta almost zero, set R=I to avoid numerical 0/0 problems
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
        if np.isnan(R).any():
            print('***** ERROR RodriguesRotationFormula')
    
    return R

#%%


def K_el_matrix(r,RT,A,Iz,Iy,It,E,G,X1,X2,e2,TC0):
    
    # Displacements in global coordinates
    
    rA=r[0:2,:]
    rB=r[6:8,:]
    L0=np.linalg.norm((X2-X1))
    L=np.linalg.norm(((X2+rB)-(X1+rA)))
    DL=L-L0
    
    # Linear strain
    epsilon=DL/L
    
    N=1*E*A*epsilon # N positive as tension
    
    # Obtain the transformation matrix
    e1=(X2-X1)/L0
    
    # Transformation matrix between global coordinates to initial (C0) configuration
    if np.isnan(TC0).any: # TC0 can be supplied as an input, skipping repeated calculations
        TC0=CoordinateTransform(e1,e2)
    
    # Transformasjon mellom initial (C0) og rotated (C0n) configuration in each node
    TC0n=CordinateTransfromInc(RT,e2,X1,X2,rA,rB,L)
    
    RTdef=np.zeros(3,3,2)
    RTdef[:,:,1-1]=TC0n*RT[:,:,1-1]*TC0.T
    RTdef[:,:,2-1]=TC0n*RT[:,:,2-1]*TC0.T
    
    # Calculate the bending deformation of the element in end A (Local coordinates)
    
    phi_a=ExRot(RTdef[:,:,0])
    phi_b=ExRot(RTdef[:,:,1])
    
    # Define the deformation vector and the axial force in the element
    
    rdef=np.vstack((np.zeros(3,1),phi_a,np.array([DL 0 0]),phi_b))
    
    # Obtain the stiffness matrix in local element coordinates
    #Material stiffness
    KKsub11=np.zeros(6,6)
    KKsub12=np.zeros(6,6)
    KKsub22=np.zeros(6,6)
    #------------------------%
    KKsub11[2-1,6-1]=6*E*Iz/(L**2)
    KKsub11[3-1,5-1]=-6*E*Iy/(L**2)
    KKsub11=KKsub11+KKsub11.T
    KKsub11[1-1,1-1]=E*A/L
    KKsub11[2-1,2-1]=12*E*Iz/(L**3)
    KKsub11[3-1,3-1]=12*E*Iy/(L**3)
    KKsub11[4-1,4-1]=G*It/L
    KKsub11[5-1,5-1]=4*E*Iy/(L)
    KKsub11[6-1,6-1]=4*E*Iz/(L)
    #------------------------%
    KKsub12[2-1,6-1]=6*E*Iz/(L**2)
    KKsub12[3-1,5-1]=-6*E*Iy/(L**2)
    KKsub12=KKsub12-KKsub12.T
    KKsub12[1-1,1-1]=-E*A/L
    KKsub12[2-1,2-1]=-12*E*Iz/(L**3)
    KKsub12[3-1,3-1]=-12*E*Iy/(L**3)
    KKsub12[4-1,4-1]=-G*It/L
    KKsub12[5-1,5-1]=2*E*Iy/(L)
    KKsub12[6-1,6-1]=2*E*Iz/(L)
    #------------------------%
    KKsub21=KKsub12.T
    #------------------------%
    KKsub22[2-1,6-1]=-6*E*Iz/(L**2)
    KKsub22[3-1,5-1]=+6*E*Iy/(L**2)
    KKsub22=KKsub22+KKsub22.T
    KKsub22[1-1,1-1]=E*A/L
    KKsub22[2-1,2-1]=12*E*Iz/(L**3)
    KKsub22[3-1,3-1]=12*E*Iy/(L**3)
    KKsub22[4-1,4-1]=G*It/L
    KKsub22[5-1,5-1]=4*E*Iy/(L)
    KKsub22[6-1,6-1]=4*E*Iz/(L)
    #------------------------%
    # Geometric stiffness
    KKGsub11=np.zeros(6,6)
    KKGsub12=np.zeros(6,6)
    KKGsub22=np.zeros(6,6)
    #------------------------%
    KKGsub11[2-1,6-1]=1/10
    KKGsub11[3-1,5-1]=-1/10
    KKGsub11=KKGsub11+KKGsub11.T
    KKGsub11[2-1,2-1]=6/5/L
    KKGsub11[3-1,3-1]=6/5/L
    KKGsub11[5-1,5-1]=2/15*L
    KKGsub11[6-1,6-1]=2/15*L
    #------------------------%
    KKGsub12[2-1,6-1]=1/10
    KKGsub12[3-1,5-1]=-1/10
    KKGsub12=KKGsub12-KKGsub12.T
    
    KKGsub12[2,2]=-6/5/L
    KKGsub12[3,3]=-6/5/L
    KKGsub12[5,5]=-1/30*L
    KKGsub12[6,6]=-1/30*L
    #------------------------%
    KKGsub21=KKGsub12.T
    #------------------------%
    KKGsub22[2,6]=-1/10
    KKGsub22[3,5]=+1/10;
    KKGsub22=KKGsub22+KKGsub22.T
    KKGsub22[2,2]=6/5/L
    KKGsub22[3,3]=6/5/L
    KKGsub22[5,5]=2/15*L
    KKGsub22[6,6]=2/15*L
    #------------------------%
    
    # Add geometric and material stiffness
    KKsub11=KKsub11  +N*KKGsub11     
    KKsub12=KKsub12  +N*KKGsub12    
    KKsub21=KKsub21  +N*KKGsub21     
    KKsub22=KKsub22  +N*KKGsub22
    
    #  Calculate the residual and the stiffness matrix in global coordinates
    
    # TT1=blkdiag_fast(TC0n,TC0n,TC0n,TC0n)
    # TT1=blkdiag_rep(TC0n,4)
    TT1=scipy.linalg.block_diag(TC0,TC0,TC0,TC0)
    
    K_el=np.array( [[KKsub11,KKsub12],[KKsub21,KKsub22]] )
    
    RHS=TT1.T*K_el*rdef
    RHSsub1=RHS[0:5,0]
    RHSsub2=RHS[6:11,0]
    
    # TT2=blkdiag_fast(TC0n,TC0n)
    #TT2=TT1(1:6,1:6)
    TT2=scipy.linalg.block_diag(TC0,TC0)
    
    KKsubGlob11=(TT2.T*[kKsub11*TT2))
    KKsubGlob12=(TT2.T*[kKsub12*TT2))
    KKsubGlob21=(TT2.T*[kKsub21*TT2))
    KKsubGlob22=(TT2.T*[kKsub22*TT2))
    
    if np.any(np.abs[k_el-K_el.T) < 1e-10)
        raise Exception('Local stiffness matrix not symmetric')
    
    
    return (RHSsub1, RHSsub2, KKsubGlob11, KKsubGlob12, KKsubGlob21, KKsubGlob22,N)
    
    %%
    
    # if sqrt(sum(sum((TC0n'*TC0n-eye(3)).**2)))>1e-12
    #     TC0n
    #     TC0n'
    #     inv(TC0n)
    #     norm(TC0n'*TC0n-eye(3))
    #     beep
    #     warning('TC0n not orthogonal')
    # end
    
    # if ne(TC0n',inv(TC0n))
    #     
    #     TC0n
    #     TC0n'
    #     inv(TC0n)
    #     beep
    #     warning('TC0n not orthogonal')
    # end
    
    # if ne(TT1',inv(TT1))
    #     beep
    #     disp('TT1 not orthogonal')
    # end
    # if ne(TT2',inv(TT2))
    #     beep
    #     disp('TT2 not orthogonal')
    # end
    
    
    
    
    



      


