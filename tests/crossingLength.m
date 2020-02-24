function crossingLength()
% calculate the path length where a line crosses an X slab
startPoint = [0,0,0];
endPoint = [30,30,30];
% the first plane is at x = 10
[point1, check] = plane_line_intersect([1,0,0],[10,0,0],startPoint,endPoint)
% the second plane is at x = 20
[point2, check] = plane_line_intersect([1,0,0],[20,0,0],startPoint,endPoint)
dist = norm(point2 - point1)
end
