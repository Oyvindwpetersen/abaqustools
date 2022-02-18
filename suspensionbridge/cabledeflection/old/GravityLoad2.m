function P=GravityLoad2(ModelInfo)

%%

P=zeros(ModelInfo.N_DOF,1);
% 
for k=1:ModelInfo.N_el

    TypeId=ModelInfo.ElementMatrix(k,4);
    
    TypeIdIndex=find(TypeId==ModelInfo.TypeId);
    
    A=ModelInfo.A(TypeIdIndex);
    rho=ModelInfo.rho(TypeIdIndex);
    TC0=ModelInfo.TC0{k};

    X1=ModelInfo.ElCoord{k}{1};
    X2=ModelInfo.ElCoord{k}{2};

    L0=norm(X2-X1);

    L0_xy=norm(X2(1:2)-X1(1:2));

    % angle with projection line in xy-plane
    alpha=atan2(X2(3)-X1(3),L0_xy);

    g=9.81;
    m=rho*A;
    q=-m*g; % load in z-direction pr unit length along the element axis

    qn=q*cos(alpha); % normal to beam
    qt=q*sin(alpha); % tangential to beam

    P_loc=L0/60*[ 
    30*qt ; 0 ; 30*qn ;
    0 ; -5*qn*L0 ; 0 ; 
    30*qt  ;  0 ; 30*qn 
    0 ; 5*qn*L0 ; 0];

    P_glob=blkdiag_rep(TC0,4).'*P_loc;

    Ind_DOF=[ModelInfo.ElDofIndex{k}{1} ModelInfo.ElDofIndex{k}{2}];
    
    P_add=zeros(size(P));
    P_add(Ind_DOF)=P_glob;

    P=P+P_add;

end

%%