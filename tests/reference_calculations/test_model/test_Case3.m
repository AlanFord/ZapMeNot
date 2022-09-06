% MATLAB script to generate a reference value used in the
% test_Case3 python unit test

function test_Case3()
    % perform a simple point-source shielding calculation
    % with buildup to verify operation of ZapMeNot
    % Problem Description:
    % - Ar-41, 3E10 Bq, located at (0,0,0)
    % - 10 cm thick iron shield
    % - 10 cm thick concrete shield
    % - Detector located at (100,0,0)
    % - Use Iron buildup factor
    % - Use air response function
    % - Ar-41 photon spectrum:
    % - MeV            Yield
    %   1.29364e+00    9.91600e-01
    %   1.67700e+00    5.15632e-04

    
    format long
    ironDensity = 7.874;   % g/cc, from the ZapMeNot material library
    concreteDensity = 2.3; % g/cc, from the ZapMeNot material library
    ironShieldThickness = 10;
    concreteShieldThickness = 10;
    bq = 3E10;
    detectorDistance = 100;
    photons = [1.29364e+00, 9.91600e-01; ...
               1.67700e+00, 5.15632e-04];

    totalExposure = 0;
    summaryData = [];
    for i = 1:length(photons(:,1))
        energy = photons(i,1);
        intensity = photons(i,2);
        ironMassAttenCoeff = getattenCoeff(energy, 'iron');
        ironMFP = ironShieldThickness * ironMassAttenCoeff * ironDensity;
        concreteMassAttenCoeff = getattenCoeff(energy, 'concrete');
        concreteMFP = concreteShieldThickness * concreteMassAttenCoeff * concreteDensity;
        mfp = ironMFP + concreteMFP;
        shieldingFactor = exp(-mfp);
        uncollidedFlux = (bq * intensity) / (4*pi()*detectorDistance^2) * shieldingFactor;
        uncollidedEnergyFlux = uncollidedFlux * energy;
        
        uncollidedPhotonExposure = uncollidedEnergyFlux * 1.835E-8 * getabsCoeff(energy);
        buildupFactor9 = buildupFactor(energy, mfp, 'iron');
        totalPhotonExposure = uncollidedPhotonExposure * buildupFactor9;

        totalExposure = totalExposure + totalPhotonExposure;
        
        newRow = [energy bq*intensity uncollidedEnergyFlux uncollidedPhotonExposure totalPhotonExposure];
        summaryData = [summaryData; newRow];
    end
    fprintf('Total Exposure = %.16g R/sec \n', totalExposure)
    fprintf('Summary data \n')
    fprintf('%.12g %.12g %.12g %.12g %.12g\n', summaryData.')    
end          
          
    