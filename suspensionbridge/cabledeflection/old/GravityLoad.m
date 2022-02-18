function P=GravityLoad(ModelInfo)

%%

P=zeros(ModelInfo.N_DOF,1);

for k=1:ModelInfo.N_el
    
    TypeId=ModelInfo.ElementMatrix(k,4);
    
    TypeIdIndex=find(TypeId==ModelInfo.TypeId);
    
    A=ModelInfo.A(TypeIdIndex);
    rho=ModelInfo.rho(TypeIdIndex);
    
	m=A*rho; % mass per meter

    P_mag=0.5*m*ModelInfo.L0(k)*9.81;
   
    Ind_dof=[ModelInfo.ElDofIndex{k}{1} ModelInfo.ElDofIndex{k}{2}];
    
    P_add=zeros(size(P));
    P_add(Ind_dof([3 6+3]))=-[ P_mag ; P_mag];
    
    P=P+P_add;

end

%%

% 
% P=zeros(size(ModelInfo.N_DOF));
% 
% for k=1:ModelInfo.N_el
%    
%     L0=norm(ModelInfo.ElInitialCoord{k}{1}-ModelInfo.ElInitialCoord{k}{2});
%     e1=ModelInfo.ElInitialCoord{k}{1}-ModelInfo.ElInitialCoord{k}{2}; e1=e1/L0;   
%     
%     ind_el=find(ModelInfo.ElementMatrix(k,1)==ModelInfo.e2mat(:,1))
%     
%     e2=ModelInfo.e2mat(ind_el,2:4);
%     
%     dx=ModelInfo.ElInitialCoord{k}{2}(1)-ModelInfo.ElInitialCoord{k}{1}(1);
%     dy=ModelInfo.ElInitialCoord{k}{2}(2)-ModelInfo.ElInitialCoord{k}{1}(2);
%     dz=ModelInfo.ElInitialCoord{k}{2}(3)-ModelInfo.ElInitialCoord{k}{1}(3);
%     
%     dproj=sqrt(dx^2+dy^2);
%     
%     alpha=atan2(dz,dproj);
%     
%     if alpha>pi/2 | alpha<-pi/2
%         error('This implementation only valid for plus minus 90 deg');
%     end
%     
%     TypeId=ModelInfo.ElementMatrix(k,4);
%     A=ModelInfo.A(TypeId);
%     rho=ModelInfo.rho(TypeId);
%     
%     m=A*rho; % mass per meter
%     q=9.81*m/cos(alpha); % load per horizontal projection
%     qn=q*cos(alpha); % normal to the element
%     qt=q*sin(alpha); % tangential to the element
%     
%     % Linear shape functions load vector
%     % Local DOF: xA,zA,rotA, xB,zB,rotB,
% %     P_loc=L/60*[30*qt ; 30*qn ; -5*qn*L ; 30*qt  ; 30*qn ; 5*qn*L ];
% %     P_loc=L/60*[30*qt ; 30*qn ; 30*qt  ; 30*qn ];
% 
%     P_loc=zeros(12,1);
%     P_loc(1)=L/60*30*qt;
%     P_loc(3)=L/60*30*qn;
%     
%     P_loc(6+1)=L/60*30*qt;
%     P_loc(6+3)=L/60*30*qn;
%     
% %     P_loc=L/60*[30*qt ; 30*qn ; 30*qt  ; 30*qn ];
% %     % To global
% %     T_temp=[cos(alpha) sin(alpha) ; -sin(alpha) cos(alpha) ];
% %     T=blkdiag(T_temp,T_temp);
% 
% 
% %     e1=(X2-X1)/L0;
%     [TC0]=CoordinateTransform(e1,e2);
% 
%     P_glob=blkdiag(TC0,TC0,TC0,TC0).'*P_loc;
%     
%     
%     Ind_dof=[ModelInfo.ElDofIndex{k}{1} ModelInfo.ElDofIndex{k}{2}];
%     
%     P_add=zeros(size(P));
%     P_add(Ind_dof)=P_glob;
%     
%     P=P+P_add;
% 
% end


%%



% syms qn m L c s
% 
% T_temp=[c s 0 ; -s c 0 ; 0 0 1];
% T=blkdiag(T_temp,T_temp);
% 
% q=m/c
% 
% qn=q*c
% qt=q*s
% 
% P_loc=L/60*[30*qt ; 30*qn ; -5*qn*L ; 30*qt  ; 30*qn ; 5*qn*L ]
% 
% P_glob=T.'*P_loc;



%%