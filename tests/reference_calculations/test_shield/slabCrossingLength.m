% MATLAB script to generate reference values 
% In test_shield.py
%   See test_crossing_length()
% Uses: 
%   plane_line_intersect.m

function slabCrossingLength()
% calculate the path length where a line crosses an X slab
format long
rayOrigin = [0,0,0];
rayEnd = [30,30,30];
planeNormal = [1,0,0];
firstEdgePoint = [10,0,0];
secondEdgePoint = [20,0,0];
[point1, check] = plane_line_intersect(planeNormal,firstEdgePoint,rayOrigin,rayEnd);
% the second plane is at x = 20
[point2, check] = plane_line_intersect(planeNormal,secondEdgePoint,rayOrigin,rayEnd);
dist = norm(point2 - point1);

fprintf('=================================\n')
fprintf('Matlab script slabCrossingLength.m\n')
fprintf('Semi-infinite slab from x= %g to x=%g \n\n', firstEdgePoint(1), secondEdgePoint(1))
fprintf('Scenario 1: Ray fully crosses slab\n')
fprintf('Ray extending from [')
fprintf('%4g', rayOrigin)
fprintf('] to [')
fprintf('%4g', rayEnd)
fprintf(']\n')
fprintf('test_crossing_length() Function: \n')
fprintf('crossing length is %.8g cmm \n\n', dist)

end
