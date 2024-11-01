from __future__ import print_function
import argparse
import os

__authors__ = ["Ilya Semennikov"]
__date__ = "20241030"
__description__ = "Directory files walker"


parser = argparse.ArgumentParser(
    description=__description__,
    epilog="Developed by {} on {}".format(
        ", ".join(__authors__), __date__)
)

parser.add_argument("DIR_PATH", help="Path to directory")
args = parser.parse_args()
path_to_scan = args.DIR_PATH

# Iterate over the path_to_scan

for root, directories, files in os.walk(path_to_scan):
    # Iterate over the files in thr current "root"
    # Create cycle into cycle
        for file_entry in files:
            # create the relative path to the file
            file_path = os.path.join(root, file_entry)
            print(file_path)