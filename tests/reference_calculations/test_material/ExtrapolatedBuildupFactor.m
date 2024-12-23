% MATLAB script to determine buildup factors for iron or concrete 
% Used by test_Case3.m
% Uses:
%   akima.m
%   alimaSlopes.m

function GP = ExtrapolatedBuildupFactor(energy, mfp, material)
    % calculate an air GP buildup factor
    % at 0.66 MeV and 10 MFP
    format long
    gpEnergy = [0.015, 0.020, 0.030, 0.040, 0.050, 0.060, 0.080, ...
                0.100, 0.150, 0.200, 0.300, 0.400, 0.500, 0.600, ...
                0.800, 1.000, 1.500, 2.000, 3.000, 4.000, 5.000, ...
                6.000, 8.000, 10.000, 15.000];
    if strcmp(material, "iron")
    gpCoeff =    [1.004, 1.561, -0.554, 5.60, 0.3524; ...
                  1.012, 0.130, 0.620, 11.39, -0.6162; ...
                  1.028, 0.374, 0.190, 29.34, -0.3170; ...
                  1.058, 0.336, 0.248, 11.65, -0.1188; ...
                  1.099, 0.366, 0.232, 14.01, -0.1354; ...
                  1.148, 0.405, 0.208, 14.17, -0.1142; ...
                  1.267, 0.470, 0.180, 14.48, -0.0974; ...
                  1.389, 0.557, 0.144, 14.11, -0.0791; ...
                  1.660, 0.743, 0.079, 14.12, -0.0476; ...
                  1.839, 0.911, 0.034, 13.23, -0.0334; ...
                  1.973, 1.095, -0.009, 11.86, -0.0183; ...
                  1.992, 1.187, -0.027, 10.72, -0.0140; ...
                  1.967, 1.240, -0.039, 8.34, -0.0074; ...
                  1.947, 1.247, -0.040, 8.20, -0.0096; ...
                  1.906, 1.233, -0.038, 7.93, -0.0110; ...
                  1.841, 1.250, -0.048, 19.49, 0.0140; ...
                  1.750, 1.197, -0.040, 15.90, 0.0110; ...
                  1.712, 1.123, -0.021, 7.97, -0.0057; ...
                  1.627, 1.059, -0.005, 11.99, -0.0132; ...
                  1.553, 1.026, 0.005, 12.93, -0.0191; ...
                  1.483, 1.009, 0.012, 13.12, -0.0258; ...
                  1.442, 0.980, 0.023, 13.37, -0.0355; ...
                  1.354, 0.974, 0.029, 13.65, -0.0424; ...
                  1.297, 0.949, 0.042, 13.97, -0.0561; ...
                  1.199, 0.957, 0.049, 14.37, -0.0594];    
    elseif strcmp(material, 'concrete')
    gpCoeff =    [1.029, 0.364, 0.240, 14.12, -0.1704; ...
                  1.067, 0.389, 0.214, 12.68, -0.1126; ...
                  1.212, 0.421, 0.201, 14.12, -0.1079; ...
                  1.455, 0.493, 0.171, 14.53, -0.0925; ...
                  1.737, 0.628, 0.115, 15.82, -0.0600; ...
                  2.125, 0.664, 0.118, 11.90, -0.0615; ...
                  2.557, 0.895, 0.042, 14.37, -0.0413; ...
                  2.766, 1.069, 0.001, 12.64, -0.0251; ...
                  2.824, 1.315, -0.049, 8.66, -0.0048; ...
                  2.716, 1.430, -0.070, 18.52, 0.0108; ...
                  2.522, 1.492, -0.082, 16.59, 0.0161; ...
                  2.372, 1.494, -0.085, 15.96, 0.0194; ...
                  2.271, 1.466, -0.082, 16.25, 0.0195; ...
                  2.192, 1.434, -0.078, 17.02, 0.0199; ...
                  2.066, 1.386, -0.073, 15.07, 0.0202; ...
                  1.982, 1.332, -0.065, 15.38, 0.0193; ...
                  1.848, 1.227, -0.047, 16.41, 0.0160; ...
                  1.775, 1.154, -0.033, 14.35, 0.0100; ...
                  1.671, 1.054, -0.010, 10.47, -0.0008; ...
                  1.597, 0.988, 0.008, 12.53, -0.0115; ...
                  1.527, 0.951, 0.020, 9.99, -0.0184; ...
                  1.478, 0.940, 0.021, 13.11, -0.0163; ...
                  1.395, 0.917, 0.028, 13.45, -0.0213; ...
                  1.334, 0.901, 0.035, 12.56, -0.0267; ...
                  1.260, 0.823, 0.065, 14.28, -0.0581];    
    elseif strcmp(material, 'air')
    gpCoeff =    [1.170, 0.459, 0.175, 13.73, -0.0862; ...
                  1.407, 0.512, 0.161, 14.40, -0.0819; ...
                  2.292, 0.693, 0.102, 13.34, -0.0484; ...
                  3.390, 1.052, -0.004, 19.76, -0.0068; ...
                  4.322, 1.383, -0.071, 13.51, 0.0270; ...
                  4.837, 1.653, -0.115, 13.66, 0.0511; ...
                  4.929, 1.983, -0.159, 13.74, 0.0730; ...
                  4.580, 2.146, -0.178, 12.83, 0.0759; ...
                  3.894, 2.148, -0.173, 14.46, 0.0698; ...
                  3.345, 2.147, -0.176, 14.08, 0.0719; ...
                  2.887, 1.990, -0.160, 14.13, 0.0633; ...
                  2.635, 1.860, -0.146, 14.24, 0.0583; ...
                  2.496, 1.736, -0.130, 14.32, 0.0505; ...
                  2.371, 1.656, -0.120, 14.27, 0.0472; ...
                  2.207, 1.532, -0.103, 14.12, 0.0425; ...
                  2.102, 1.428, -0.086, 14.35, 0.0344; ...
                  1.939, 1.265, -0.057, 14.24, 0.0232; ...
                  1.835, 1.173, -0.039, 14.07, 0.0161; ...
                  1.712, 1.051, -0.011, 13.67, 0.0024; ...
                  1.627, 0.983, 0.006, 13.51, -0.0051; ...
                  1.558, 0.943, 0.017, 13.82, -0.0117; ...
                  1.505, 0.915, 0.025, 16.37, -0.0231; ...
                  1.418, 0.891, 0.032, 12.06, -0.0167; ...
                  1.358, 0.875, 0.037, 14.01, -0.0226; ...
                  1.267, 0.844, 0.048, 14.55, -0.0344]; 
    end      
    b = akima(log(gpEnergy), gpCoeff(:,1), log(energy));
    c = akima(log(gpEnergy), gpCoeff(:,2), log(energy));
    a = akima(log(gpEnergy), gpCoeff(:,3), log(energy));
    X = akima(log(gpEnergy), gpCoeff(:,4), log(energy));
    d = akima(log(gpEnergy), gpCoeff(:,5), log(energy));
    if mfp <= 0
        mfp = 0;
    end
    if mfp > 80
        mfp = 80;
    end
    if mfp <= 40
        K = (c * (mfp^a)) + (d * (tanh(mfp/X -2) - tanh(-2))) / (1 - tanh(-2));
    else
        K35 = (c * (35^a)) + (d * (tanh(35/X -2) - tanh(-2))) / (1 - tanh(-2));
        K40 = (c * (40^a)) + (d * (tanh(40/X -2) - tanh(-2))) / (1 - tanh(-2));
        fm = 0.8;
        Xi = (((mfp/35)^0.1)-1) / (((40/35)^0.1)-1);
        testVal = (K40-1)/(K35-1);
        if testVal >= 0 && testVal <= 1
            K = 1 + (K35-1) * (((K40-1)/(K35-1))^Xi);
        else
            K = K35 * (K40/K35)^(Xi^fm);
        end
    end
    if K == 1
        GP = 1 + (b-1)*mfp;
    else
        GP = 1 + (b-1)*((K^mfp) - 1)/(K -1);
    end
end