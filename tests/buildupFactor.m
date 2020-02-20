function buildupFactor()
% calculate an air GP buildup factor
% at 0.66 MeV and 10 MFP
energy = 0.66
mfp = 10
lowCoeffs =  [2.377e+00, 1.679e+00, -1.240e-01, 1.423e+01, 5.030e-02]
highCoeffs = [2.212e+00, 1.544e+00, -1.050e-01, 1.436e+01, 4.370e-02]
lowEnergy = 0.6
highEnergy = 0.8

fraction = (energy-lowEnergy)/(highEnergy-lowEnergy)
coeffs = fraction*(highCoeffs-lowCoeffs) + lowCoeffs
b = coeffs(1)
c = coeffs(2)
a = coeffs(3)
X = coeffs(4)
d = coeffs(5)

K = (c * (mfp^a)) + (d * (tanh(mfp/X -2) - tanh(-2))) / (1 - tanh(-2))

if K == 1
    GP = 1 + (b-1)*mfp
else
    GP = 1 + (b-1)*((K^mfp) - 1)/(K -1)

end