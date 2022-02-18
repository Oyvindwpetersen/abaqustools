function [theta_vec]=ExRot(R)

%%  Algorithm for rotation tensor to rotation vector

% Following Eq (2.12) in Bruheim

d1=0.5*(R(3,2)-R(2,3));
d2=0.5*(R(1,3)-R(3,1));
d3=0.5*(R(2,1)-R(1,2));

theta=asin(sqrt(d1^2+d2^2+d3^2));

% Set to factor when angle is small
if abs(theta)<1e-12
    factor=1; % Factor set 1 (not 0), bug fix
%     disp('Exrot factor')
else
    factor=theta/sin(theta);
end

theta_vec=factor*[d1 d2 d3]';

%% Test

% [e]=SarabandiThomas(R);
% quat=quaternion(e);
% theta_vec2=rotvec(quat).';
% 
% theta_vec=theta_vec2;