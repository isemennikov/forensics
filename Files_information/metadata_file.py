from __future__ import print_function
import argparse
from datetime import datetime as dt
import os
import sys
from idlelib.outwin import file_line_pats

from Files_information.ja import parsers

# Default args
_authors__ = ["Ilya Semennikov"]
__date__ = "2024015"
__description__ = "Gatharing filesystem metadata of provide files"

parser = argparse.ArgumentParser(
    description = __description__,
    epilog="Developed by {} on {}".format(", ".join(_authors__), __date__)
)

# Add Positional Arguments
parser.add_argument("FILE_PATH",
                    help="Path to file to gather metadata for")
args = parser.parse_args()
file_path = args.FILE_PATH
