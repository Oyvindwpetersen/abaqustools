function [RHSsub1, RHSsub2, KKsubGlob11, KKsubGlob12, KKsubGlob21, KKsubGlob22,N]=K_el_matrix(r,RT,A,Iz,Iy,It,E,G,X1,X2,e2,TC0)

%% Displacements in global coordinates

rA=r(1:3,:);
rB=r(7:9,:);
L0=sqrt((X2-X1)'*(X2-X1));
L=sqrt(((X2+rB)-(X1+rA))'*((X2+rB)-(X1+rA)));
DL=L-L0;
%DL=2/(L+L0)*((X2+rB)-(X1+rA)-1/2*(rB-rA))'*(rB-rA);

% Linear strain
epsilon=DL/L;

% Green strain
% epsilon=DL/L+0.5*(DL/L)**2;

N=1*E*A*epsilon; % N positive as tension


%% Obtain the transformation matrix

e1=(X2-X1)/L0;

% Transformation matrix between global coordinates to initial (C0) configuration
if isempty(TC0) % TC0 can be supplied as an input, skipping repeated calculations
    [TC0]=CoordinateTransform(e1,e2);
end

% Transformasjon mellom initial (C0) og rotated (C0n) configuration in each node
[TC0n]=CordinateTransfromInc(RT,e2,X1,X2,rA,rB,L);

RTdef=zeros(3,3,2);
RTdef(:,:,1)=TC0n*RT(:,:,1)*TC0';
RTdef(:,:,2)=TC0n*RT(:,:,2)*TC0';

%% Calculate the bending deformation of the element in end A (Local coordinates)

[phi_a]=ExRot(RTdef(:,:,1));
[phi_b]=ExRot(RTdef(:,:,2));

%% Define the deformation vector and the axial force in the element

rdef=[zeros(3,1); phi_a; [DL 0 0]'; phi_b];

%% Obtain the stiffness matrix in local element coordinates
%Material stiffness
KKsub11=zeros(6,6);
KKsub12=zeros(6,6);
KKsub22=zeros(6,6);
%------------------------%
KKsub11(2,6)=6*E*Iz/(L**2);
KKsub11(3,5)=-6*E*Iy/(L**2);
KKsub11=KKsub11+KKsub11';
KKsub11(1,1)=E*A/L;
KKsub11(2,2)=12*E*Iz/(L**3);
KKsub11(3,3)=12*E*Iy/(L**3);
KKsub11(4,4)=G*It/L;
KKsub11(5,5)=4*E*Iy/(L);
KKsub11(6,6)=4*E*Iz/(L);
%------------------------%
KKsub12(2,6)=6*E*Iz/(L**2);
KKsub12(3,5)=-6*E*Iy/(L**2);
KKsub12=KKsub12-KKsub12';
KKsub12(1,1)=-E*A/L;
KKsub12(2,2)=-12*E*Iz/(L**3);
KKsub12(3,3)=-12*E*Iy/(L**3);
KKsub12(4,4)=-G*It/L;
KKsub12(5,5)=2*E*Iy/(L);
KKsub12(6,6)=2*E*Iz/(L);
%------------------------%
KKsub21=KKsub12';
%------------------------%
KKsub22(2,6)=-6*E*Iz/(L**2);
KKsub22(3,5)=+6*E*Iy/(L**2);
KKsub22=KKsub22+KKsub22';
KKsub22(1,1)=E*A/L;
KKsub22(2,2)=12*E*Iz/(L**3);
KKsub22(3,3)=12*E*Iy/(L**3);
KKsub22(4,4)=G*It/L;
KKsub22(5,5)=4*E*Iy/(L);
KKsub22(6,6)=4*E*Iz/(L);
%------------------------%
% Geometric stiffness
KKGsub11=zeros(6,6);
KKGsub12=zeros(6,6);
KKGsub22=zeros(6,6);
%------------------------%
KKGsub11(2,6)=1/10;
KKGsub11(3,5)=-1/10;
KKGsub11=KKGsub11+KKGsub11';
KKGsub11(2,2)=6/5/L;
KKGsub11(3,3)=6/5/L;
KKGsub11(5,5)=2/15*L;
KKGsub11(6,6)=2/15*L;
%------------------------%
KKGsub12(2,6)=1/10;
KKGsub12(3,5)=-1/10;
KKGsub12=KKGsub12-KKGsub12';

KKGsub12(2,2)=-6/5/L;
KKGsub12(3,3)=-6/5/L;
KKGsub12(5,5)=-1/30*L;
KKGsub12(6,6)=-1/30*L;
%------------------------%
KKGsub21=KKGsub12';
%------------------------%
KKGsub22(2,6)=-1/10;
KKGsub22(3,5)=+1/10;
KKGsub22=KKGsub22+KKGsub22';
KKGsub22(2,2)=6/5/L;
KKGsub22(3,3)=6/5/L;
KKGsub22(5,5)=2/15*L;
KKGsub22(6,6)=2/15*L;
%------------------------%

% Add geometric and material stiffness
KKsub11=KKsub11  +N*KKGsub11;        
KKsub12=KKsub12  +N*KKGsub12;        
KKsub21=KKsub21  +N*KKGsub21;       
KKsub22=KKsub22  +N*KKGsub22;

%%  Calculate the residual and the stiffness matrix in global coordinates

% TT1=blkdiag_fast(TC0n,TC0n,TC0n,TC0n);
TT1=blkdiag_rep(TC0n,4);

K_el=[KKsub11 KKsub12; KKsub21 KKsub22];

RHS=TT1'*K_el*rdef;
RHSsub1=RHS(1:6,1);
RHSsub2=RHS(7:12,1);

% TT2=blkdiag_fast(TC0n,TC0n);
TT2=TT1(1:6,1:6);

KKsubGlob11=(TT2'*(KKsub11*TT2)); KKsubGlob12=(TT2'*(KKsub12*TT2)); KKsubGlob21=(TT2'*(KKsub21*TT2)); KKsubGlob22=(TT2'*(KKsub22*TT2));

if isempty(nonzeros(K_el-K_el'))==0
    beep
    disp('Local stiffness matrix not symmetric')
    return
end

%%

if sqrt(sum(sum((TC0n'*TC0n-eye(3)).**2)))>1e-12
    TC0n
    TC0n'
    inv(TC0n)
    norm(TC0n'*TC0n-eye(3))
    beep
    warning('TC0n not orthogonal')
end

% if ne(TC0n',inv(TC0n))
%     
%     TC0n
%     TC0n'
%     inv(TC0n)
%     beep
%     warning('TC0n not orthogonal')
% end

% if ne(TT1',inv(TT1))
%     beep
%     disp('TT1 not orthogonal')
% end
% if ne(TT2',inv(TT2))
%     beep
%     disp('TT2 not orthogonal')
% end



