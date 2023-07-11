% Copyright (c) 2009, Greg von Winckel
% All rights reserved.
% 
% Redistribution and use in source and binary forms, with or without
% modification, are permitted provided that the following conditions are
% met:
% 
%     * Redistributions of source code must retain the above copyright
%       notice, this list of conditions and the following disclaimer.
%     * Redistributions in binary form must reproduce the above copyright
%       notice, this list of conditions and the following disclaimer in
%       the documentation and/or other materials provided with the distribution
% 
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
% AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
% IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
% ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
% LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
% CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
% SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
% INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
% CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
% ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
% POSSIBILITY OF SUCH DAMAGE.
function [r,t,p,w]=spherequad(nr,nt,np,rad)

%SPHEREQUAD  Generate Gauss quadrature nodes and weights for numerically
% computing spherical volume integrals.
%
% [R,T,P,W]=SPHEREQUAD(NR,NT,NP,RAD) computes the product grid nodes in
% r, theta, and phi in spherical and the corresponding quadrature weights
% for a sphere of radius RAD>0. NR is the number of radial nodes, NT is
% the number of theta angle nodes in [0,pi], and NP is the number of phi 
% angle nodes in [0, 2*pi]. The sphere radius RAD can be set to infinity, 
% however, the functions to be integrated must decay exponentially with 
% radius to obtain a reasonable numerical approximation.
%
% Example 1: Infinite domain, theta independent
%
% f=@(R,T,P) exp(-R.^2.*(2+sin(P))); 
% [R,T,P,W]=spherequad(50,1,30,inf);
% Q=W'*f(R,T,P);
%
% Example 2: Sphere of radius 2, depends on all three
%
% f=@(R,T,P) sin(T.*R).*exp(-R.*sin(P));
% [R,T,P,W]=spherequad(24,24,24,2);
% Q=W'*f(R,T,P);
%
% Written by: Greg von Winckel - 04/13/2006
% Contact: gregvw(at)math(dot)unm(dot)edu 
% URL: http://www.math.unm.edu/~gregvw


[r,wr]=rquad(nr,2);         % radial weights and nodes (mapped Jacobi)

if rad==inf                 % infinite radius sphere
   
    wr=wr./(1-r).^4;        % singular map of sphere radius
    r=r./(1-r);
    
else                        % finite radius sphere
    
    wr=wr*rad^3;            % Scale sphere radius
    r=r*rad;
    
end

[x,wt]=rquad(nt,0); 
t=acos(2*x-1); wt=2*wt;     % theta weights and nodes (mapped Legendre)
p=2*pi*(0:np-1)'/np;        % phi nodes (Gauss-Fourier)
wp=2*pi*ones(np,1)/np;      % phi weights
[rr,tt,pp]=meshgrid(r,t,p); % Compute the product grid
r=rr(:); t=tt(:); p=pp(:);

w=reshape(reshape(wt*wr',nr*nt,1)*wp',nr*nt*np,1);


% function [x,w]=rquad(N,k)
% 
% k1=k+1; k2=k+2; n=1:N;  nnk=2*n+k;
% A=[k/k2 repmat(k^2,1,N)./(nnk.*(nnk+2))];
% n=2:N; nnk=nnk(n);
% B1=4*k1/(k2*k2*(k+3)); nk=n+k; nnk2=nnk.*nnk;
% B=4*(n.*nk).^2./(nnk2.*nnk2-nnk2);
% ab=[A' [(2^k1)/k1; B1; B']]; s=sqrt(ab(2:N,2));
% [V,X]=eig(diag(ab(1:N,1),0)+diag(s,-1)+diag(s,1));
% [X,I]=sort(diag(X));    
% x=(X+1)/2; w=(1/2)^(k1)*ab(1,2)*V(1,I)'.^2;