% MATLAB script to generate source point locations in cylindrical geometry
% for a z-aligned cylinder centered on the origin

function [dots] = generic_cylinder(points, length, radius)
    % this defines the number of source points [ r, theta, z]
    format long
    % points = [3 3 3];
    center = [0 0 0];
    % length = 10;
    % radius = 5;
    % determine the cross-sectional area
    area = pi()*radius^2;

    % NOTE: theta and radial locations are zero based.
    %       Z locations are not!

    % determine the z locations, assuming the center is at (0,0,0)
    zStart = -(length/2);
    zLocations = linspace(1,points(3),points(3));
    zLocations = zLocations .* length/points(3);
    zLocations = zLocations - length/points(3)/2;
    zLocations = zLocations + zStart;

    % determine the theta locations
    thetaDelta = 2*pi/points(2);
    thetaLocations = linspace(1,points(2),points(2));
    thetaLocations = thetaLocations .* thetaDelta;
    thetaLocations = thetaLocations - thetaDelta/2;

    % determine the radial locations based on uniform area
    circleAreas = linspace(0,points(1),points(1)+1) ...
        *area/points(1); % area of each concentric circle
    rBoundaries = sqrt(circleAreas/pi); % radii of concentric circles
    rMids = zeros(points(1),1);
    for i = 1:points(1)
        rMids(i) = (rBoundaries(i+1)+rBoundaries(i))/2;
    end
    % convert everthing from cylindrical to cartesian coordinates
    dots = [];
    for i=1:points(1)
        for j=1:points(2)
            for k=1:points(3)
                [x,y,z] = pol2cart(thetaLocations(j), rMids(i), zLocations(k));
                % now shift to the (x,y) origin
                x = x + center(1);
                y = y + center(2);
                z = z + center(3);
                dots = [dots;[x, y, z]];
            end
        end
    end
end
