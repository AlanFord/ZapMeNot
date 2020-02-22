function buildupFactor()
    % calculate an air GP buildup factor
    % at 0.66 MeV and 10 MFP
    energy = 0.66;
    mfp = 10;
    lowCoeffs =  [2.371, 1.656, -0.120, 14.27, 0.0472];
    highCoeffs = [2.207, 1.532, -0.103, 14.12, 0.0425];

    lowEnergy = 0.6;
    highEnergy = 0.8;

    fraction = (energy-lowEnergy)/(highEnergy-lowEnergy);
    coeffs = fraction*(highCoeffs-lowCoeffs) + lowCoeffs;
    b = coeffs(1);
    c = coeffs(2);
    a = coeffs(3);
    X = coeffs(4);
    d = coeffs(5);

    K = (c * (mfp^a)) + (d * (tanh(mfp/X -2) - tanh(-2))) / (1 - tanh(-2));

    if K == 1
        GP = 1 + (b-1)*mfp
    else
        GP = 1 + (b-1)*((K^mfp) - 1)/(K -1)
    end
end