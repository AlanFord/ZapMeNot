% MATLAB script to test the uncollided dose of 1 MeV photons distributed
% in a sphere of radius 10 cm.
% Quadrature uses 10 divisions in all dimensions.
% Sphere has an origin at x=4, y=6, z=6.
% Dose point is 20 cm from the origin of the sphere.
% Phonton source is 1 MeV at 1 Bq (1 photon/sec)
% Source and shielding materials are air with a density
%   of 1.00e-10 g/cm3 (intended to be low enough to be negligible)
origin = [ 4 5 6];
dosePoint = [4 5 26];
radius = 10;
nRadial = 10;
nAzimuthal = 10; % 0 - 2*pi
nPolar = 10; % 0 - pi

[r,t,p,w]=spherequad(nRadial,nPolar,nAzimuthal,radius);

% cartesian coordinates with sphere centered at the origin
x = r.*sin(t).*cos(p);
y = r.*sin(t).*sin(p);
z = r.*cos(t);
w = w./sum(w);  % make the weights fractional volumes

% cartesian coordinates with sphere centered at [origin]
locations = [x, y, z];
locations = locations + repmat(origin, size(x,1),1);

% calculate distances from dose point
dosePoints = repmat(dosePoint, size(x,1),1);
distances = dosePoints - locations;
lengths = sqrt(sum(distances.^2,2));

% calculate dose
airMassEnAbsCoeff = 2.787E-02; % @ 1MeV (ANS 6.4.3 Table 2)
mfp = 0;
sourceBq = 1;
shieldingFactor = exp(-mfp);  % should be 1
uncollidedFlux = sourceBq .* w ./ (4*pi().*lengths.^2) * shieldingFactor;
uncollidedEnergyFlux = uncollidedFlux .* 1; % 1 MeV
uncollidedExposure = uncollidedEnergyFlux .* 1.835E-8 .* airMassEnAbsCoeff;
finalExposure = sum(uncollidedExposure);
finalExposure = finalExposure .*(1000*3600) % convert from R/sec to mR/hr
