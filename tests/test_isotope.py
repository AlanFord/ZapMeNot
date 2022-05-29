import pytest

from zap_me_not import isotope

pytestmark = pytest.mark.basic

# request an invalid material
# reference: none required
def test_a_bad_isotope_name():
	with pytest.raises(ValueError):
		a = isotope.Isotope("wanker")

# test using a capitalized isotope name and mixed-case name
# reference: none required
def test_name_case():
	try:
		a = isotope.Isotope("CO-60")
	except ValueError:
		pytest.fail("All caps isotope name failed")
	try:
		a = isotope.Isotope("Co-60")
	except ValueError:
		pytest.fail("Mixed-case isotope name failed")
	try:	
		a = isotope.Isotope("co-60")
	except ValueError:
		pytest.fail("Lower case isotope name failed")

# test valid half life in years
# reference: isotope library and hand calculation
def test_halflife():
	# years
	a = isotope.Isotope("co-60")
	assert  a.half_life == pytest.approx(5.2711*365.25*24*60*60)
	# days
	a = isotope.Isotope("Ac-225")
	assert  a.half_life == pytest.approx(10*24*60*60)
	# hours
	a = isotope.Isotope("cu-67")
	assert a.half_life == pytest.approx(2.57630*24*60*60)
	# minutes
	a = isotope.Isotope("Ag-105m")
	assert a.half_life == pytest.approx(7.23000*60)
	# seconds
	a = isotope.Isotope("Ag-109m")
	assert a.half_life == pytest.approx(39.6)
	# milliseconds
	# >>> nothing to test in library
	# microseconds
	# >>> nothing to test in library

# test valid photon property read and store
# reference: isotope library
def test_photon_readAndStore():
	a = isotope.Isotope("co-60")
	assert a.photons ==[[3.47140e-01, 7.50000e-05], \
						[8.26100e-01, 7.60000e-05], \
						[1.17320e+00, 9.98500e-01], \
						[1.33250e+00, 9.99830e-01], \
						[2.15860e+00, 1.20000e-05], \
						[2.50570e+00, 2.00000e-08]]



