function [TC0n]=CordinateTransfromInc(RT,e2,X1,X2,rA,rB,L)

%%

% Vector along deformed element
e1=((X2+rB)-(X1+rA))/L

% The e2 direction is the e2 rotated for each node, then averaged over the new e2 directions for these two nodes
e2a=RT[:,:,1]*e2
e2b=RT[:,:,2]*e2
e2ab=1*(e2a+e2b)

% e3=CrossProduct(e1,e2ab)
e3=cross(e1,e2ab)

e3=e3/sqrt(e3'*e3)
% e2=CrossProduct(e3,e1)
e2=cross(e3,e1)

TC0n=CoordinateTransform(e1,e2)
