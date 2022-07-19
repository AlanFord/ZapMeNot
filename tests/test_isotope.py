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
	assert  a.half_life == pytest.approx(5.27130*365.25*24*60*60)
	# days
	a = isotope.Isotope("Ac-225")
	assert  a.half_life == pytest.approx(10*24*60*60)
	# hours
	a = isotope.Isotope("cu-67")
	assert a.half_life == pytest.approx(6.18300e+01*60*60)
	# minutes
	a = isotope.Isotope("Ag-105m")
	assert a.half_life == pytest.approx(7.23000*60)
	# seconds
	a = isotope.Isotope("Ag-109m")
	assert a.half_life == pytest.approx(39.6)
	# milliseconds
	a = isotope.Isotope("Ra-219")
	assert a.half_life == pytest.approx(10*1e-3)
	# microseconds
	a = isotope.Isotope("Rn-215")
	assert a.half_life == pytest.approx(2.3*1e-6)

# test valid photon property read and store
# reference: isotope library
def test_photon_readAndStore():
	a = isotope.Isotope("co-60")
	assert a.photons ==[[3.47140e-01, 7.50000e-05], \
						[8.26100e-01, 7.60000e-05], \
						[1.17323e+00, 9.98500e-01], \
						[1.33249e+00, 9.99826e-01], \
						[2.15857e+00, 1.20000e-05], \
						[2.50569e+00, 2.00000e-08]]

# test retrieval of key progeny
# reference: isotope library
def test_progeny_readAndStore():
	a = isotope.Isotope("Ce-144")
	assert a.key_progeny == {"Pr-144":0.999993,"Pr-144m":0.0954780}

# test retrieval of key progeny from isotope that has none
# reference: isotope library
def test_blank_progeny():
	a = isotope.Isotope("O-19")
	assert a.key_progeny == None




