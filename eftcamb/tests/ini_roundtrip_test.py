"""Optional regression reproducer for the upstream ini read/write interface.

Run separately from the installation smoke tests while investigating the known
native-finalization and parameter-cache round-trip issues.
"""

import tempfile
import unittest
from pathlib import Path

import eftcamb


class IniRoundTripTest(unittest.TestCase):
    def test_ini_round_trip_uses_package_cli(self):
        parameters = eftcamb.set_params(H0=67.4, ombh2=0.0224, omch2=0.12)
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "parameters.ini"
            parameters.write_ini(filename)
            # EFTCAMB change Start
            restored = eftcamb.read_ini(str(filename))
            # EFTCAMB change End
        self.assertAlmostEqual(restored.H0, parameters.H0)
