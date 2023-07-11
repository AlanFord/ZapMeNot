% MATLAB script to test the generation of spherical volume quadrature

[r_ref, w_ref] = rquad(8,2)

nRadial = 4;
nPolar = 5; % 0 - pi
nAzimuthal = 6; % 0 - 2*pi
radius = 10;
[r,t,p,w]=spherequad(nRadial,nPolar,nAzimuthal,radius)

nRadial = 1; nPolar = 1; nAzimuthal = 1; radius = 10;
[r1,t1,p1,w1]=spherequad(nRadial,nPolar,nAzimuthal,radius)
