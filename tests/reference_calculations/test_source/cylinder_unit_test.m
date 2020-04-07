% MATLAB script to generate source point locations in cylindrical geometry 
% In test_source.py
%   See TestZAlignedCylinderSource.test_getSourcePoints()
% Uses:

function cylinder_unit_test()
% this defines the number of source points [ r, theta, z]
format long
points = [3 3 3];
center = [0 0 0];
length = 10;
radius = 5;
% determine the cross-sectional area
area = pi()*radius^2;
% determine the total volume
volume = area*length;

% determine the z locations
zLocations = linspace(1,points(3),points(3));
zLocations = zLocations .* length/points(3);
zLocations = zLocations - length/points(3)/2

% determine the theta locations
thetaDelta = 2*pi/points(2);
thetaLocations = linspace(1,points(2),points(2));
thetaLocations = thetaLocations .* thetaDelta;
thetaLocations = thetaLocations - thetaDelta/2

% determine the radial locations based on uniform area
radialIntervalArea = area/points(1);  %uniform area of each radial ring
circleAreas = linspace(0,points(1),points(1)+1) ...
    *area/points(1); % area of each concentric circle
rBoundaries = sqrt(circleAreas/pi); % radii of concentric circles
for i = 1:points(1)
    rMids(i) = (rBoundaries(i+1)+rBoundaries(i))/2;
end

% convert everthing from cylindrical to cartesian coordinates
for i=1:points(1)
    for j=1:points(2)
        for k=1:points(3)
            [x,y,z] = pol2cart(thetaLocations(j), rMids(i), zLocations(k));
            fprintf("%.10d %.10d %.10d\n",x,y,z)
        end
    end
end
end
