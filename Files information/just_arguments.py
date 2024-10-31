from __future__ import print_function
import argparse

__authors__ == ["Ilya Semennikov"]
__date__ = "20241030"
__descripton__ = "A simple argparse example"

parsers = argparse.ArgumentParser(
    description=__descripton__,
    epilog="Developed by {} on {}".format(
        ", ".join(__authors__), __date__)
    )

# Add Positional Arguments

parsers.add_argument("INPUT_FILE", help="Path to input files")
parsers.add_argument("OUTPUT_FILE", help="Path to output file")

#Optional arguments
parsers.add_argument("--hash", help="Hash the files",action="store_true")
parsers.add_argument("--hash-algoritm", help="Hash algoritm to use SHA1 or/and SHA256", choices=['SHA1', 'SHA256'], default="SHA256")

