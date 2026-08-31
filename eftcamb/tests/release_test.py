"""Release smoke tests for the standalone H-EFTCAMB distribution."""

# EFTCAMB MOD START: cover standalone import, GR/RPH calculations, CLI isolation, and CAMB coexistence for release artifacts.
import importlib.util
import subprocess
import sys
import unittest

import numpy as np

import eftcamb


def make_gr_parameters():
    """Return a minimal, stable GR-limit H-EFTCAMB configuration."""
    return eftcamb.set_params(
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


def make_rph_parameters():
    """Return the fixed RPH configuration from ``BasicEFTExample.yaml``."""
    return eftcamb.set_params(
        H0=67.0,
        ombh2=0.0222,
        omch2=0.12,
        mnu=0.06,
        YHe=0.245,
        As=2.1e-9,
        ns=0.965,
        dark_energy_model="EFTCAMB",
        EFTflag=2,
        AltParEFTmodel=1,
        RPHwDE=0,
        RPHusealphaM=True,
        RPHkineticitymodel_ODE=2,
        RPHbraidingmodel_ODE=2,
        RPHalphaMmodel_ODE=2,
        RPHkineticity_ODE0=0.01,
        RPHbraiding_ODE0=0.5,
        RPHalphaM_ODE0=1.0,
        EFT_ghost_math_stability=False,
        EFT_mass_math_stability=False,
        EFT_ghost_stability=True,
        EFT_gradient_stability=True,
        EFT_positivity_bounds=False,
        EFT_additional_priors=True,
        EFTCAMB_turn_on_time=0.1,
        EFTCAMB_stability_time=0.1,
        feedback_level=0,
    )


class ReleaseSmokeTest(unittest.TestCase):
    def assert_finite_background(self, parameters):
        results = eftcamb.get_background(parameters)
        redshifts = np.array([0.0, 0.5, 1.0])
        hubble = results.hubble_parameter(redshifts)
        distances = results.comoving_radial_distance(redshifts)
        self.assertTrue(np.all(np.isfinite(hubble)))
        self.assertTrue(np.all(np.isfinite(distances)))
        self.assertAlmostEqual(float(hubble[0]), parameters.H0, places=8)
        self.assertEqual(float(distances[0]), 0.0)
        return results

    def test_gr_limit_background(self):
        self.assert_finite_background(make_gr_parameters())

    def test_rph_background(self):
        self.assert_finite_background(make_rph_parameters())

    def test_command_line_version_does_not_import_standard_camb(self):
        completed = subprocess.run(
            [sys.executable, "-m", "eftcamb._command_line", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.stdout.strip(), eftcamb.__version__)

        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys, eftcamb; assert 'camb' not in sys.modules; print(eftcamb.__file__)",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("eftcamb", completed.stdout)

    @unittest.skipUnless(importlib.util.find_spec("camb"), "requires camb==1.6.5")
    def test_camb_and_eftcamb_can_calculate_in_one_process(self):
        import camb

        camb_parameters = camb.set_params(
            H0=67.4,
            ombh2=0.0224,
            omch2=0.12,
            mnu=0.06,
            YHe=0.245,
            As=2.1e-9,
            ns=0.965,
        )
        camb_results = camb.get_background(camb_parameters)
        eft_results = self.assert_finite_background(make_gr_parameters())

        self.assertNotEqual(camb.__file__, eftcamb.__file__)
        self.assertNotEqual(camb.baseconfig.CAMBL, eftcamb.baseconfig.CAMBL)
        self.assertTrue(np.isfinite(camb_results.hubble_parameter(0.0)))
        self.assertTrue(np.isfinite(eft_results.hubble_parameter(0.0)))
# EFTCAMB MOD END
