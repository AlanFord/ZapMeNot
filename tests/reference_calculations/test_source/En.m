function a =En(n,x)
% calculates the exponential integral for shielding
% see page F1 of "The Photon Shielding Manual" by A Foderaro
if n==1 
    a = expint(x);
else
    a = expint(x);
    for i=2:n
        new = (exp(-x)- x*a)/(i-1);
        a = new;
    end
end

end