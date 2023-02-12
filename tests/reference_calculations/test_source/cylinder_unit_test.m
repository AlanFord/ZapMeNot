% MATLAB script to generate source point locations in cylindrical geometry
% for a z-aligned cylinder
% In test_source.py
%   See TestZAlignedCylinderSource.test_getSourcePoints()
% Uses:

% this defines the number of source points [ r, theta, z]
format long
points = [3 3 3];
center = [-1 2 3];
length = 10;
radius = 5;

dots = generic_cylinder(points, length, radius);

% x-aligned cylinder
% rotate (x replaced by z; z replaced by -x)
newDots = dots;
newDots(:,1)  = dots(:,3);
newDots(:,2)  = dots(:,2);
newDots(:,3)  = -dots(:,1);
% shift
xDots = newDots + center
% fprintf("\nx-aligned cylinder\n")
% fprintf("%.10d %.10d %.10d\n",newDots)

% y-aligned cylinder
% rotate (y replaced by z; z replaced by -y)
newDots = dots;
newDots(:,1)  = dots(:,1);
newDots(:,2)  = dots(:,3);
newDots(:,3)  = -dots(:,2);
% shift
yDots = newDots + center
% fprintf("\ny-aligned cylinder\n")
% fprintf("%.10d %.10d %.10d\n",newDots)

% z-aligned cylinder
% rotation not needed
newDots = dots;
% shift to new center
zDots = newDots + center
% fprintf("\nz-aligned cylinder\n")
% fprintf("%.10d %.10d %.10d\n",newDots)
