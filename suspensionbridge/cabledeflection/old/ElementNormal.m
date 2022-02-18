function [e2mat,e3mat]=ElementNormal(ElementMatrix,NodeMatrix)

%%

for k=1:size(ElementMatrix,1)
    
NodeNumber=ElementMatrix(k,2:3);

Index1=find(NodeMatrix(:,1)==NodeNumber(1));
Index2=find(NodeMatrix(:,1)==NodeNumber(2));

if isempty(Index1)
    error(['Node not found: ' num2str(NodeNumber(1)) ]);
end

if isempty(Index2)
    error(['Node not found: ' num2str(NodeNumber(2)) ]);
end



X1=NodeMatrix(Index1,2:4);
X2=NodeMatrix(Index2,2:4);

if size(X1,1)<size(X1,2)
    X1=X1.';
end

if size(X2,1)<size(X2,2)
    X2=X2.';
end


e1=X2-X1;
e1=e1/norm(e1);
e3_guess=[0 0 1].';

e2=cross(e3_guess,e1);
e2=e2/norm(e2);

e3=cross(e1,e2);
e3=e3/norm(e3);


e2mat(k,2:4)=e2;
e3mat(k,2:4)=e3;

e2mat(k,1)=ElementMatrix(k,1);
e3mat(k,1)=ElementMatrix(k,1);

end