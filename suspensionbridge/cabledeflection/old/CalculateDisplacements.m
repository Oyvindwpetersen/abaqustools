function [r,KT_red]=CalculateDisplacements(KT,P,ModelInfo)

%%

% Eliminate DOFs not used
KT_red=KT(ModelInfo.IndexInclude,ModelInfo.IndexInclude);
P_red=P(ModelInfo.IndexInclude);

% Solve
r_red=KT_red\P_red;

% Repopulate to all DOFs
r=ModelInfo.S_red*r_red;

