% MATLAB script to test the extrapolation
% of buildup factors

function getAirExtrapolation()
    energy = 0.033865;
    mfp =  45;
    material = 'air';
    for I = 1 : length(mfp)
        GP(I) = ExtrapolatedBuildupFactor(energy, mfp(I), material);
        % GPold(I) = OldExtrapolatedBuildupFactor(energy, mfp(I), material);
    end
    mfp
    format longE
    transpose(GP)
