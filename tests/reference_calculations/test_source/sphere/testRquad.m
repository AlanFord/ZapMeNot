% MATLAB script to test the rquad function, used in the 
% generation of spherical volume quadrature

[r_ref, w_ref] = rquad(8,2)
[r_ref1, w_ref1] = rquad(8,0)
[r_ref2, w_ref2] = rquad(1,2)
[r_ref3, w_ref3] = rquad(1,0)

