import argparse
import ctypes
import os
import sys
from argparse import RawTextHelpFormatter

# EFTCAMB MOD START: use only package-local imports so the CLI does not load standard CAMB.
from . import __version__
from .baseconfig import lib_import
# EFTCAMB MOD END


def run_command_line():
    # EFTCAMB MOD START: present H-EFTCAMB CLI help and version information to users.
    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="Python command line H-EFTCAMB reading parameters from a .ini file."
        + "\n\nSample .ini files are provided in the source distribution, "
        "e.g. see inifiles/planck_2018.ini at "
        "https://github.com/LinSJ-astronomy/EFTCAMB-MSJ/tree/pypi-publish/inifiles",
    )
    parser.add_argument("ini_file", help="text .ini file with parameter settings")
    parser.add_argument(
        "--validate", action="store_true", help="Just validate the .ini file, dont actually run anything"
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)
    args = parser.parse_args()

    if not os.path.exists(args.ini_file):
        sys.exit(f"File not found: {args.ini_file}")
    # EFTCAMB MOD END

    s = ctypes.create_string_buffer(args.ini_file.encode("latin-1"))

    # Import wrapper function round fortran command line program
    CAMB_RunCommandLine = lib_import("camb", "camb", "CommandLineValidate" if args.validate else "CommandLineRun")
    CAMB_RunCommandLine.argtypes = [ctypes.c_char_p, ctypes.c_long]
    CAMB_RunCommandLine(s, ctypes.c_long(len(args.ini_file)))
    if args.validate:
        print("OK")


if __name__ == "__main__":
    run_command_line()
