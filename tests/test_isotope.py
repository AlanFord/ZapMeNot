import pytest

from ZapMeNot import isotope

pytestmark = pytest.mark.basic

# request an invalid material
def test_a_bad_isotope_name():
	with pytest.raises(ValueError):
		a = isotope.Isotope("wanker")

# test using a capitalized isotope name and mixed-case name
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
def test_halflife():
	# years
	a = isotope.Isotope("co-60")
	assert  a.half_life == pytest.approx(5.271*365.25*24*60*60)
	# days
	a = isotope.Isotope("Ac-225")
	assert  a.half_life == pytest.approx(10*24*60*60)
	# hours
	a = isotope.Isotope("cu-67")
	assert a.half_life == pytest.approx(61.86*60*60)
	# minutes
	a = isotope.Isotope("c-11")
	assert a.half_life == pytest.approx(20.38*60)
	# seconds
	a = isotope.Isotope("Ag-109m")
	assert a.half_life == pytest.approx(39.6)
	# milliseconds
	a = isotope.Isotope("At-215")
	assert a.half_life == pytest.approx(0.1/1000)
	# microseconds
	a = isotope.Isotope("Po-212")
	assert a.half_life == pytest.approx(0.305/1000/1000)

# test valid photon property read and store
def test_photon_readAndStore():
	a = isotope.Isotope("co-60")
	assert a.photons ==[[3.46930e-01, 7.59999e-05], \
						[8.26280e-01, 7.59999e-05], \
						[1.17321e+00, 9.99000e-01], \
						[1.33247e+00, 9.99824e-01], \
						[2.15877e+00, 1.10000e-05], \
						[2.50500e+00, 3.60000e-08]]



