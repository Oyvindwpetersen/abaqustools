function [RHS,KT,N]=Assembly(r,RT,ModelInfo)

%%

N_nodes=size(ModelInfo.NodeMatrix,1)
N_NodeDof=6;
N_el=size(ModelInfo.ElementMatrix,1)

K=spalloc(N_NodeDof*N_nodes,N_NodeDof*N_nodes,ceil(0.01*N_NodeDof^2*N_nodes^2))

RHS=zeros(N_NodeDof*N_nodes,1)

N=zeros(N_el,1)

for k=1:N_el
    
    % Index of all DOFs to DOFs in nodes
    n=ModelInfo.ElDofIndex[k]{1};
    m=ModelInfo.ElDofIndex[k]{2};

    % Initial coordinates of nodes
    X1=ModelInfo.ElCoord[k]{1}.';
    X2=ModelInfo.ElCoord[k]{2}.';

    % Lateral vector
    e2=ModelInfo.e2mat(k,2:4)';

    % Cross sectional properties
    ElementType=ModelInfo.ElementMatrix(k,4)
    ElementTypeIndex=find(ModelInfo.TypeId==ElementType)
    
    A=ModelInfo.A(ElementTypeIndex]
    Iz=ModelInfo.Iz(ElementTypeIndex]
    Iy=ModelInfo.Iy(ElementTypeIndex]
    It=ModelInfo.It(ElementTypeIndex]
    E=ModelInfo.E(ElementTypeIndex]
    G=ModelInfo.G(ElementTypeIndex]
    rho=ModelInfo.rho(ElementTypeIndex]
    TC0=ModelInfo.TC0[k];

    % Node numbers and index for element
    NodeNumber=[ModelInfo.ElementMatrix(k,2) ModelInfo.ElementMatrix(k,3)];
    NodeIndex(1)=find(ModelInfo.NodeMatrix(:,1)==NodeNumber(1))
    NodeIndex(2)=find(ModelInfo.NodeMatrix(:,1)==NodeNumber(2))

    % Get matrix
    [RHSsub1,RHSsub2,K_el_sub11,K_el_sub12,K_el_sub21,K_el_sub22,N_el]=K_el_matrix(r([n m],:),RT(:,:,NodeIndex),A,Iz,Iy,It,E,G,X1,X2,e2,TC0)

    % Assign to global stiffness matrix  
%     K(n,n)=K(n,n)+K_el_sub11;
%     K(n,m)=K(n,m)+K_el_sub12;
%     K(m,n)=K(m,n)+K_el_sub21;
%     K(m,m)=K(m,m)+K_el_sub22;
    
    % Assign to global stiffness matrix (faster)
    K([n m],[n m])=K([n m],[n m])+[ K_el_sub11 K_el_sub12 ; K_el_sub21 K_el_sub22];
    
    % Axial force
    N(k)=N_el;
    
    
    % RHS
    RHS(n,:)=RHS(n,:)+RHSsub1;
    RHS(m,:)=RHS(m,:)+RHSsub2;

end

KT=K;



