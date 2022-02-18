function [RT]=IncrementalRotation(r,RT)


for n=1:size(r,1)/6

    RotInc(1,1)=r(6*n-2,1);
    RotInc(2,1)=r(6*n-1,1);
    RotInc(3,1)=r(6*n,1);

    R=RodriguesRotationFormula(RotInc);

    RT(:,:,n)=R*RT(:,:,n);
end


end

%%

function [R]=RodriguesRotationFormula(theta_vec)

% Implemented as Eq.(2.10) in Bruheim
% See also https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula

% Find scalar magnitude
theta=sqrt(theta_vec'*theta_vec);

% If theta almost zero, set R=I to avoid numerical 0/0 problems
if theta<1e-10
    R=eye(3);
else
    n_vec=theta_vec/theta;
    
    % Spin matrix
    N=zeros(3,3);
    N(1,2)=-n_vec(3,1);
    N(1,3)=n_vec(2,1);
    N(2,3)=-n_vec(1,1);
    N=N-N';
    
    R=eye(3)*cos(theta)+N*sin(theta)+(1-cos(theta))*(n_vec*n_vec'); 
    if sum(sum(isnan(R)))>0
        beep
        theta_vec
        theta
        R=[]
    end
end

end





      
