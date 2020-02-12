class Source(Shield):
	"""Abtract class to model a radiation source."""
	pass

class PointSource(Source):
	"""Modeling a point source of radiation."""
	pass

class LineSource(Source):
	"""Modeling a finite-length line source of radiation."""
	pass

class PlaneSource(Source):
	"""Modeling a finite-area planar source of radiation."""
	pass