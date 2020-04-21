function answer = endShieldedCyl(R0,h,a,us,b1,bq,E)
% arguments:
% R0 = radius of cylinder
% h = height of cylinder
% a = distance between cylinder face and dose point on the cylinder axis
% us = linear attenuation coefficient of the source material (cm-1)
% b1 = total linear attuenuation coeff of all shields (cm-1)
% bq = source strength in Bq
% E = energy of photons in MeV

theta = atan(R0/a); % angle subtended by cylinder
Sv = bq/(h*pi*R0^2); % volumetric source (Bq/cm3/sec)
b3 = b1 + us*h;
% calculate xi
if us*R0 > 4
    xi = theta;
else
    if h/R0 <= 1
        thetaPrime = atan(R0/(a+h));
        xi = (theta+thetaPrime)/2;
    else
        ratio = xiRatio(a*R0, us*R0, b1);
        xi = ratio*theta;
    end
end
    
answer
end