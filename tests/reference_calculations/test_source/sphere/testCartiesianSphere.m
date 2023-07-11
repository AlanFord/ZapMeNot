% MATLAB script to test the generation of cartesian points translated
% from spherical quadrature.  Cartesian Z and Spherical Z are colocated
origin = [ 4 5 6];
radius = 13;
nRadial = 4;
nAzimuthal = 6; % 0 - 2*pi
nPolar = 5; % 0 - pi

[r,t,p,w]=spherequad(nRadial,nPolar,nAzimuthal,radius);

% cartesian coordinates with sphere centered at the origin
x = r.*sin(t).*cos(p)
y = r.*sin(t).*sin(p)
z = r.*cos(t)
w = w

% cartesian coordinates with sphere centered at [origin]
locations = [x, y, z]
locations = locations + repmat(origin, size(x,1),1)


