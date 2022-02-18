function [r,KT,K_add,RHS,R_NL,N]=NonLinearSolver(ModelInfo,P_loadstep,varargin)

%% 

%% Parse inputs

p=inputParser;
addParameter(p,'IncrementType','linear')
addParameter(p,'LoadIncrements',10)
addParameter(p,'IterationMax',100)
addParameter(p,'ShowText',true)
addParameter(p,'PlotNorm',true)
addParameter(p,'norm_tol',1e-10)
addParameter(p,'LinearStiffness',[])


if norm_tol>1
    error('')
end

%% Load step scaling

if strcmpi(IncrementType,'exp') % a*exp(b*n)
    f_scale=logspace(-6,0,LoadIncrements)
end

if LoadIncrements==1
    f_scale=1;
end

%% Multiple load cases (propagating analysis)

LoadSteps=length(P_loadstep)

%% Direct additions to stiffness matrix

if ~isempty(LinearStiffness)
    K_add=sparse(LinearStiffness{1}(:,1),LinearStiffness{1}(:,2),LinearStiffness{2},ModelInfo.N_DOF,ModelInfo.N_DOF)
else
    K_add=sparse(ModelInfo.N_DOF,ModelInfo.N_DOF)
end

%% Initialization

RT=zeros(3,3,ModelInfo.N_DOF)
for n=1:ModelInfo.N_DOF; RT(:,:,n)=eye(3,3) end

r=zeros(ModelInfo.N_DOF,1)

%% Iterative calculations

norm_dr={};
norm_dr_iter={};

t0=tic()

for j=1:LoadSteps
    
stardisp(['Load step ' num2str(j,'%0.2d') '/' num2str(LoadSteps,'%0.2d')],1)

P=P_loadstep{j};

if j==1
    P_prev_loadstep=zeros(size(P_loadstep{j}))
    P_add=P_loadstep{j};
else
    P_prev_loadstep=P_loadstep{j-1};
    P_add=P_loadstep{j}-P_prev_loadstep;
end


for l=1:LoadIncrements

    stardisp(['Load increment ' num2str(l,'%0.2d') '/' num2str(LoadIncrements,'%0.2d')],1) 
    
    % Load for this step
%     fn=f_scale(l)*P;
    fn=P_prev_loadstep+f_scale(l)*P_add; % Add load: from previos load step plus difference*scalefactor, where scale factor [0,1]
    
    % Some initial for convergence check
    norm_dr{l,j}(1)=NaN; 
    norm_dr_iter{l,j}(1)=NaN; 
    
    n=0;
    LoadIncrementConv=false;
    while n<IterationMax && LoadIncrementConv==false
        
        n=n+1;
        
        if ShowText; stardisp(['Iteration ' num2str(n,'%0.2d') '']) end
        
        % Build model
        [RHS,KT,N]=Assembly(r,RT,ModelInfo)

        % Added stiffness
        if ~isempty(LinearStiffness)
            KT=KT+K_add;
        end
        
        % Residual
        Rn=fn-RHS;
        
        % Increment calculation
        [dr,KT_red]=CalculateDisplacements(KT,Rn,ModelInfo)
        [RT]=IncrementalRotation(dr,RT)
        
        % If norm of dr is too large, decrease
        if norm(dr)>max(norm_dr_iter{l,j})
        stardisp(['norm(dr) large, dr scaled down' ''])
        scale_iter=0.5;
        else
        scale_iter=1;
        end
        
        % Update response
        r=r+dr*scale_iter;
    
        % Check if converged
        if norm(dr)/(ModelInfo.N_DOF)<norm_tol
            LoadIncrementConv=true;
        end

        % Save norms
        norm_dr{l}(n)=norm(dr)
        norm_dr_iter{l,j}(n)=norm(dr*scale_iter)

    end

    if LoadIncrementConv==false
        stardisp(['Break simulation at load increment ' num2str(l,'%0.2d') '/' num2str(LoadIncrements,'%0.2d'), ', applied load ratio ' num2str(f_scale(l)) ])
        warning('Not converged')
        break
    end
    
end

r_step{j}=r;

end
t1=toc(t0)

stardisp(['Calculation time ' num2str(t1,'%0.2d') '']) 



%% Outputs

