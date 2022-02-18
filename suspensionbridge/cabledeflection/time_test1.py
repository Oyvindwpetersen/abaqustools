# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 17:07:27 2022

@author: oyvinpet
"""
#%%

from Assembly import Assembly

#%%


t0=numtools.tic()

for n in range(100):
    # A=sparse.csr_matrix(K_el)
    # A=sparse.csr_matrix((1000,1000))
    #A = sparse.dok_matrix((1000,1000))
    #A = sparse.lil_matrix((1000,1000))
   # A = sparse.coo_matrix((1000,1000))
    
    A=np.zeros((1000,1000))
    for k in range(500):
    
        #A[2*1:2*1+2,2*1:2*1+2]=A[2*1:2*1+2,2*1:2*1+2]+np.eye(2)
       A[2*k:2*k+2,2*k:2*k+2]+=np.eye(2)
        # row=np.arange(1'2)
        # n=m
        # col=n+m
        # data=np.ones(len(row))
        # S_el=sparse.csr_matrix((data, (row, col)),shape=(len(row),np.shape(K)[0])) #.toarray()
    
        # a=S_el.T @  K_el2 #@ S_el
    
    
    A=sparse.csr_matrix(A)
numtools.toc(t0)

#%% Time stack methodology

K_el_sub11=np.eye(2)
K_el_sub12=np.eye(2)*10
K_el_sub21=np.eye(2)*100
K_el_sub22=np.eye(2)*200

t0=numtools.tic()
for n in range(10000):
        K_el=np.vstack( (np.hstack([K_el_sub11,K_el_sub12]),np.hstack([K_el_sub21,K_el_sub22])) )
numtools.toc(t0)


t0=numtools.tic()
for n in range(10000):
        K_el=np.block([[K_el_sub11,K_el_sub12],[K_el_sub21,K_el_sub22]])
numtools.toc(t0)

t0=numtools.tic()
for n in range(10000):
        K_el=np.concatenate( (np.concatenate((K_el_sub11,K_el_sub12),axis=1),np.concatenate((K_el_sub21,K_el_sub22),axis=1)),axis=0)
numtools.toc(t0)



#%% Block diagonal

A=np.random.randn(6,6)
import scipy

t0=numtools.tic()
for n in range(10000):
        c1=scipy.linalg.block_diag(A,A,A,A)
numtools.toc(t0)

t0=numtools.tic()
for n in range(10000):
        c2=numtools.block_diag_rep_old(A,4)
numtools.toc(t0)

t0=numtools.tic()
for n in range(10000):
        c3=numtools.block_diag_rep(A,4)
numtools.toc(t0)

#%% Stack

e1=np.array([0,1,0])
e2=np.array([10,20,30])
e3=np.array([100,200,300])

t0=numtools.tic()
for n in range(100000):
        T=np.vstack((e1,e2,e3))
numtools.toc(t0)


t0=numtools.tic()
for n in range(100000):
        T2=np.array([e1,e2,e3])
numtools.toc(t0)


#%% Stack vector


phi_a=np.ones(3)
phi_b=np.ones(3)
DL=100.0

t0=numtools.tic()
for n in range(10000):
    rdef=np.hstack((np.zeros((3)),phi_a,np.array([DL,0,0]),phi_b))
numtools.toc(t0)


t0=numtools.tic()
for n in range(10000):
    rdef2=np.concatenate((np.zeros((3)),phi_a,np.array([DL,0,0]),phi_b),axis=0)
numtools.toc(t0)


#%% Norm

u=np.array([1,2.0,3.0])
v=np.array([3,1.0,3.0])

t0=numtools.tic()
for n in range(1000000):
    s1 = np.linalg.norm(u)
numtools.toc(t0)

t0=numtools.tic()
for n in range(1000000):
    s2 = numtools.norm_fast(u)
numtools.toc(t0)

t0=numtools.tic()
for n in range(1000000):
    #s2 = sum(u**2)**0.5
    s2 = sum(u*u)**0.5
    #s2 = math.sqrt(sum(u*u))

numtools.toc(t0)

#%% Cross


u=np.array([1,2,3])
v=np.array([3,1,3])

t0=numtools.tic()
for n in range(10000):
    s1 = np.cross(u,v)
numtools.toc(t0)

t0=numtools.tic()
for n in range(10000):
    s2 = numtools.cross_fast(u,v)
numtools.toc(t0)



u=np.array([[1,2,3]]).T
v=np.array([[3,1,3]]).T

t0=numtools.tic()
for n in range(10000):
    eijk = np.zeros((3, 3, 3))
    eijk[0, 1, 2] = eijk[1, 2, 0] = eijk[2, 0, 1] = 1
    eijk[0, 2, 1] = eijk[2, 1, 0] = eijk[1, 0, 2] = -1

    s3 = np.einsum('iuk,vk->uvi', np.einsum('ijk,uj->iuk', eijk, u), v)
numtools.toc(t0)



#%% Stack in 3D

TC0=np.ones((3,3))
TC0n=np.ones((3,3))-0.5

RT_sub=np.ones((3,3,2))-0.1

t0=numtools.tic()
for n in range(10000):
    RTdef=np.zeros((3,3,2))
    RTdef[:,:,0]=TC0n @ RT_sub[:,:,0] @ TC0.T
    RTdef[:,:,1]=TC0n @ RT_sub[:,:,1] @ TC0.T
numtools.toc(t0)

t0=numtools.tic()
for n in range(10000):
    RTdef=np.dstack((TC0n @ RT_sub[:,:,0] @ TC0.T,TC0n @ RT_sub[:,:,1] @ TC0.T))
numtools.toc(t0)

#%% Fill matrix

n_vec=np.array([1,2,3])

t0=numtools.tic()
for n in range(1000000):
        # Spin matrix
        N=np.zeros((3,3))
        N[1-1,2-1]=-n_vec[3-1]
        N[1-1,3-1]=n_vec[2-1]
        N[2-1,3-1]=-n_vec[1-1]
        N=N-N.T
numtools.toc(t0)

t0=numtools.tic()
for n in range(1000000):
        # Spin matrix
        N=np.array([ [0,-n_vec[2],n_vec[1]],
                    [n_vec[2],0,-n_vec[0]],
                    [-n_vec[1],n_vec[0],0]]
                   )
numtools.toc(t0)


#%% Multiply in 3D


n=3
m=3
j=3
k=100
A=np.random.random((n,m,k))
B=np.random.random((m,j,k))

t0=numtools.tic()
for n in range(1000):
    C1=np.tensordot(A,B, axes = ((1),(0)))
    
numtools.toc(t0)

t0=numtools.tic()
for n in range(1000):
    C2=np.einsum('nmk,mjk->njk',A,B)
numtools.toc(t0)

t0=numtools.tic()
for n in range(1000):
    C3=np.zeros((np.shape(C2)))
    for ind in range(k):
        C3[:,:,ind]=A[:,:,ind] @ B[:,:,ind]
numtools.toc(t0)


#%% Incremental rotation
# Use the Rotation function in scipy rather than self written

n_node=100
r=np.random.random(6*n_node)/100
RT=np.random.random((3,3,n_node))/100

for k in range(n_node):
    RT[:,:,k]=np.eye(3)

t0=numtools.tic()
for n in range(1000):
    C1=Corot.IncrementalRotation_old(r,RT)
numtools.toc(t0)

t0=numtools.tic()
for n in range(1000):
    C2=Corot.IncrementalRotation(r,RT)
numtools.toc(t0)

check=np.allclose(C1,C2)
print(check)

#%% Exrot

R=np.random.random((3,3))/100

t0=numtools.tic()
for n in range(10000):
    C1=Corot.ExRot(R)
numtools.toc(t0)

t0=numtools.tic()
for n in range(10000):
    C2=Corot.ExRot_fast(R)
numtools.toc(t0)

check=np.allclose(C1,C2)
print(check)

#%% Check rotation matrix Rodrigues

v=np.array([-0.2, 0.1, 0.05])

v=v/numtools.norm_fast(v)

t0=numtools.tic()
for n in range(10000):
    r1=Rotation.from_rotvec(v).as_matrix()
numtools.toc(t0)

t0=numtools.tic()
for n in range(10000):
    r2=Corot.RodriguesRotationFormula(v)
numtools.toc(t0)

check=np.allclose(r1,r2)
print(check)

#%%

#%%

e1=np.array([0,1,0.1])
e2=np.array([0.3,1,0])

t0=numtools.tic()
for n in range(100000):
    r2=Corot.CoordinateTransform(e1,e2)
numtools.toc(t0)

t0=numtools.tic()
for n in range(100000):
    r3=Corot.CoordinateTransform_old(e1,e2)
numtools.toc(t0)


check=np.allclose(r2,r3)
print(check)

#%%


R2=np.zeros(np.shape(RT))
for n in np.arange(int(len(r)/6)):
        
    RotInc=np.zeros(3)
    
    RotInc[1-1]=r[6*(n+1)-2-1]
    RotInc[2-1]=r[6*(n+1)-1-1]
    RotInc[3-1]=r[6*(n+1)-1]
    
    R2[:,:,n]=RodriguesRotationFormula(RotInc)
    
RT_out2=np.einsum('nmk,mjk->njk',R,RT)





#%%
a=np.random.randn(3,3)

t0=numtools.tic()
for n in range(1000):
    A=[None]*100
    for k in range(100):
        A[k]=a*k
    B=np.dstack(A)
numtools.toc(t0)

t0=numtools.tic()
for n in range(1000):
    A=[a*k for k in range(100)]
    B=np.dstack(A)
numtools.toc(t0)

t0=numtools.tic()
for n in range(1000):
    A=[a*k for k in range(100)]
    B=np.dstack(A)
numtools.toc(t0)



t0=numtools.tic()
for n in range(1000):
    A=[a*k for k in range(100)]
numtools.toc(t0)


t0=numtools.tic()
for n in range(1000):
    B2=np.zeros((3,3,100))
    for k in range(100):
        B2[:,:,k]=a*k
numtools.toc(t0)