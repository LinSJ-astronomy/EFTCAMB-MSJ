==========
H-EFTCAMB
==========

:Project: Effective Field Theory for CAMB
:Python package: ``eftcamb``
:Source: https://github.com/LinSJ-astronomy/EFTCAMB-MSJ

H-EFTCAMB is an effective-field-theory extension of CAMB for calculating
cosmological observables in modified-gravity models.  Its Python interface
wraps the numerical Fortran implementation and follows the familiar CAMB-style
parameter and results API.

Installation
============

Install a published binary wheel with::

    python -m pip install eftcamb

The first independent release targets macOS and Linux wheels.  On a platform
without a suitable wheel, install from source with a compatible Fortran
compiler, BLAS, and LAPACK available on ``PATH``.

Quick start
===========

The published distribution is imported as ``eftcamb``::

    import eftcamb

    parameters = eftcamb.set_params(
        H0=67.4,
        ombh2=0.0224,
        omch2=0.12,
        mnu=0.06,
        YHe=0.245,
        As=2.1e-9,
        ns=0.965,
        dark_energy_model="EFTCAMB",
        EFTflag=0,
    )
    results = eftcamb.get_background(parameters)
    print(results.hubble_parameter(0.0))

``EFTflag=0`` selects the GR limit.  H-EFTCAMB-specific model parameters can
then be supplied through ``set_params`` in the same way as the examples in the
source repository.

Command-line interface
======================

The package also provides an ``eftcamb`` command.  For example::

    eftcamb --version

The command-line interface uses the package-local H-EFTCAMB library and does
not require the standard CAMB Python package.

Coexistence with CAMB
=====================

H-EFTCAMB may be installed in the same environment as the upstream package::

    python -m pip install camb==1.6.5 eftcamb

The two distributions use different Python module names and separate native
libraries.  They can therefore be imported and used in the same Python process::

    import camb
    import eftcamb

Building from source
====================

Clone the repository with its submodules and install it from the checkout::

    git clone --recurse-submodules https://github.com/LinSJ-astronomy/EFTCAMB-MSJ.git
    cd EFTCAMB-MSJ
    python -m pip install .

For a direct Fortran build, use ``make python`` in the ``fortran/`` directory.
The resulting native library is written to the ``eftcamb`` package directory.

Licensing and attribution
=========================

H-EFTCAMB is a modification of CAMB.  The distribution includes the root
``LICENCE.txt``, the H-EFTCAMB licence at ``fortran/eftcamb/LICENSE``, and the
bundled ForUtils licence at ``forutils/LICENSE``.  Please retain the relevant
citations and licence notices when using or redistributing the software.
