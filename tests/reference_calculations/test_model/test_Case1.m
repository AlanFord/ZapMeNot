% MATLAB script to generate reference values 
% In test_model.py
%   See test_Case1()
% Uses: 

function test_Case1()
    % perform a simple point-source shielding calculation
    % with buildup to verify operation of ZapMeNot
    % Problem Description:
    % - 1 MeV point source, 3E10 Bq, located at (0,0,0)
    % - 10 cm thick iron shield
    % - 10 cm thick concrete shield
    % - Detector located at (100,0,0)
    % - Use Iron buildup factor
    % - Use air response function
    
    format long
    ironDensity = 7.874;   % g/cc, from the ZapMeNot material library
    concreteDensity = 2.3; % g/cc, from the ZapMeNot material library
    airDensity = 0.001205; % g/cc, from the ZapMeNot material library
    airMassEnAbsCoeff = 2.787E-02; % @ 1MeV (ANS 6.4.3 Table 2)
    ironMassAttenCoeff = 5.957E-02; % @ 1MeV (ANS 6.4.3 Table 1a)
    concreteMassAttenCoeff = 6.368E-02; % @ 1MeV (ANS 6.4.3 Table 1a)
    % G-P Buildup Factor Coefficients @ 1MeV (ANS 6.4.3 Table 5.1)
    %               b      c       a     Xk     d
    ironGP =     [1.841, 1.250, -0.048, 19.49, 0.0140];
    b = ironGP(1);
    c = ironGP(2);
    a = ironGP(3);
    Xk = ironGP(4);
    d = ironGP(5);
    
    
    ironMFP = 10 * ironMassAttenCoeff * ironDensity
    concreteMFP = 10 * concreteMassAttenCoeff * concreteDensity
    mfp = ironMFP + concreteMFP;

    K = (c * (mfp^a)) + (d * (tanh(mfp/Xk -2) - tanh(-2))) / (1 - tanh(-2));

    if K == 1
        ironBuildupFactor = 1 + (b-1)*mfp;
    else
        ironBuildupFactor = 1 + (b-1)*((K^mfp) - 1)/(K -1);
    end
    shieldingFactor = exp(-mfp);
    uncollidedFlux = 3E10 / (4*pi()*100^2) * shieldingFactor
    uncollidedEnergyFlux = uncollidedFlux * 1
    uncollidedExposure = uncollidedEnergyFlux * 1.835E-8 * airMassEnAbsCoeff
    totalExposure = uncollidedExposure * ironBuildupFactor

end          
          
    