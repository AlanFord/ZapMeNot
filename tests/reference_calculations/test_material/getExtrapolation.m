% MATLAB script to test the extrapolation
% of buildup factors

function getExtrapolation()
    energy = 2.9;
    mfp =  [1 5 10 15 20 25 30 35 39.9 40.1 45 50 55 60 61 70];
    material = 'iron';
    for I = 1 : length(mfp)
        GP(I) = ExtrapolatedBuildupFactor(energy, mfp(I), material);
    end
    mfp
    GP
    plot(mfp, GP)
