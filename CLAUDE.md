# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZapMeNot is a Python library for point-kernel photon shielding analyses. It calculates radiation exposure at detector locations from various source geometries, accounting for photon attenuation through shielding materials using the point-kernel method. The library includes benchmark cases validated against Microshield calculations.

## Development Commands

### Testing
```bash
# Run basic unit tests
pytest -m basic

# Run benchmark cases (designed to fail and show % difference from Microshield)
pytest -s -m benchmark

# Run graphics/display tests
pytest -m graphics
```

### Building and Installation
```bash
# Install in development mode
pip install -e .

# Build distribution
hatch build

# Install from local source
pip install .
```

### Documentation
The project uses Sphinx for documentation generation. Documentation source files are in `docsrc/` and the built documentation is in `docs/`.

## Code Architecture

### Point-Kernel Method
The library implements point-kernel photon shielding analysis by:
1. Discretizing source volumes into quadrature points
2. Tracing rays from each source point to detector locations
3. Calculating attenuation through shields along each ray path
4. Integrating contributions from all source points

### Core Components

**Model** (`model.py`) - The central orchestrator that:
- Combines sources, shields, and detectors into a complete analysis
- Manages the `calculate_exposure()` workflow which iterates over photon energies and source points
- Uses numpy arrays for vectorized calculations across all source points simultaneously
- Calculates crossing distances through each shield for every source-detector ray
- Applies buildup factors to account for scattered radiation

**Source Classes** (`source.py`) - Radiation source geometries:
- All sources inherit from both `Source` and `Shield` (sources attenuate their own emissions)
- Provide `_get_source_points()` returning quadrature locations within the source volume
- Provide `_get_source_point_weights()` returning fractional volumes for integration
- Support isotopes (from library) and individual photons
- Photon grouping options: `discrete`, `group`, or `hybrid` (groups when count exceeds threshold)
- Key progeny can be automatically included via `include_key_progeny` property
- Source types: `PointSource`, `LineSource`, `SphereSource`, `BoxSource`, and axis-aligned cylinder sources
- `SphereSource` uses specialized spherical quadrature (`_spherequad`) for accurate volume integration

**Shield Classes** (`shield.py`) - Photon barrier geometries:
- All shields implement `_get_crossing_length(ray)` to compute ray intersection distances
- Support both finite geometries (boxes, spheres, cylinders) and infinite/semi-infinite (slabs, annuli)
- Shells are hollow spherical shields (represented as two nested spheres)
- Ray-geometry intersection logic uses analytical methods (line-plane, ray-sphere, ray-box algorithms)
- `is_infinite()` and `is_hollow()` methods inform visualization bounds

**Material** (`material.py`) - Photon interaction properties:
- Loads material data from `materialLibrary.yml` (mass attenuation coefficients, buildup factors, densities)
- Provides interpolated values via Akima splines for arbitrary photon energies
- Buildup factors use the G-P (Geometric Progression) fitting method
- Supports custom material densities (override library defaults)

**Detector** (`detector.py`) - Simple point location for exposure calculation

**Isotope** (`isotope.py`) - Radionuclide decay data:
- Loads isotope data from a library file
- Provides photon emission spectra with energies and intensities
- Supports key progeny relationships

**Ray** (`ray.py`) - Vector mathematics for ray tracing between source points and detectors

### Integration and Quadrature
- Box and cylinder sources use uniform Cartesian grids
- Sphere sources use specialized spherical quadrature that accounts for non-uniform volume elements
- Line sources use 1D linear quadrature
- Quadrature weights sum to 1.0, representing volume fractions

### Visualization
Optional PyVista integration provides 3D visualization:
- `Model.display()` renders sources, shields, and detectors
- Infinite shields are clipped to a bounding box based on finite geometry extents
- Point sources and detectors displayed as small spheres (2.5% of minimum dimension)

### Benchmark Cases
Benchmarks in `benchmarks/` compare ZapMeNot calculations against Microshield:
- Tests are marked with `@pytest.mark.benchmark`
- Intentionally fail to display percent difference from reference calculations
- Each benchmark has a corresponding Jupyter notebook in `benchmarks/workbooks/`

## Material Library
The `materialLibrary.yml` file contains photon interaction data for various materials. When adding or modifying materials, validation scripts are in `dataConversion/materialLibraryValidation/`.

## Important Notes
- Source points and detector locations must never be coincident (raises ValueError)
- Shields should not overlap (detected by negative gap distances)
- The filler material fills all non-shield regions between source and detector
- Buildup factor material is typically the dominant shield material
- Exposure units: mR/hr (output), activity units: Bq or Curies (input)
- All geometry uses Cartesian coordinates (cm)
