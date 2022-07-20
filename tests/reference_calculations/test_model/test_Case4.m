% MATLAB script to generate a reference value used in the
% test_Case4 python unit test

function test_Case4()
    % perform a simple point-source shielding calculation
    % with buildup to verify operation of ZapMeNot
    % Problem Description:
    % - Co-60, 3 Ci, located at (1, 2, 3)
    % - 10 cm thick iron shield
    % - 10 cm thick concrete shield
    % - Detector located at (80,90,100)
    % - Use Iron buildup factor
    % - Use air response function
    % - Co-60 photon spectrum:
    % - MeV            Yield
    %   3.47140e-01    7.50000e-05
    %   8.26100e-01    7.60000e-05
    %   1.17323e+00    9.98500e-01
    %   1.33249e+00    9.99826e-01
    %   2.15857e+00    1.20000e-05
    %   2.50569e+00    2.00000e-08

    
    format long
    ironDensity = 7.874;   % g/cc, from the ZapMeNot material library
    concreteDensity = 2.3; % g/cc, from the ZapMeNot material library
    bq = 3 * 3.7E10;
    photons = [3.47140e-01,    7.50000e-05; ...
               8.26100e-01,    7.60000e-05; ...
               1.17323e+00,    9.98500e-01; ...
               1.33249e+00,    9.99826e-01; ...
               2.15857e+00,    1.20000e-05; ...
               2.50569e+00,    2.00000e-08];
    source = [1 2 3];
    detector = [80 90 100];
    detectorDistance = norm(detector-source);
    ironDistance = norm(plane_line_intersect([1 0 0],[10 0 0],source,detector)- ...
                        plane_line_intersect([1 0 0],[20 0 0],source,detector))
    concreteDistance = norm(plane_line_intersect([1 0 0],[30 0 0],source,detector)- ...
                            plane_line_intersect([1 0 0],[40 0 0],source,detector))

    totalExposure = 0;
    for i = 1:length(photons(:,1))
        energy = photons(i,1);
        intensity = photons(i,2);
        ironMassAttenCoeff = getattenCoeff(energy, 'iron');
        ironMFP = ironDistance * ironMassAttenCoeff * ironDensity;
        concreteMassAttenCoeff = getattenCoeff(energy, 'concrete');
        concreteMFP = concreteDistance * concreteMassAttenCoeff * concreteDensity;
        mfp = ironMFP + concreteMFP;
        shieldingFactor = exp(-mfp);
        uncollidedFlux = (bq * intensity) / (4*pi()*detectorDistance^2) * shieldingFactor;
        buildupFactor9 = buildupFactor(energy, mfp, 'iron');
        buildupFlux = uncollidedFlux * buildupFactor9;
        exposure = buildupFlux * 1.835E-8 * energy * getabsCoeff(energy);
        totalExposure = totalExposure + exposure;
    end
fprintf('Total Exposure = %.16g R/sec \n', totalExposure)
    

end          
          
    