function [T]=CoordinateTransform(e1,e2)

%% Description

% This routine calculates the rotation matrix R that transforms a vector a
% from a cordinate system defined by the orthogonal base vectors E1,E2,E3
% to a coordinate system defined by the orthogonal vectors e1,e2 and e3 for
% reference see Kolbein Bell "Matrise Statikk"

%%

% Check dim
if size(e1,1)==1; e1=e1'; end
if size(e2,1)==1; e2=e2'; end

% Normalize
e1=e1/sqrt(e1'*e1);
e2=e2/sqrt(e2'*e2);

% Crossproduct
e3=cross(e1,e2);

T=[e1'; e2'; e3'];

%% Check orthogonality

if abs(dot(e1,e2))>1.0e-10
   beep
   warning('Unit vectors e1 and e2 are not orthogonal' )
   warning(['The dot product is ' num2str(dot(e1,e2)) ])
   return
end

if abs(dot(e1,e3))>1.0e-10
    beep
   warning('Unit vectors e1 and e3 are not orthogonal' )
   warning(['The dot product is ' num2str(dot(e1,e3)) ])
   return
end

if abs(dot(e2,e3))>1.0e-10
    beep
   warning('Unit vectors e2 and e3 are not orthogonal' )
   warning(['The dot product is ' num2str(dot(e1,e3)) ])
   return
end

