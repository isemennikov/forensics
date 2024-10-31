from __future__ import print_function
import argparse
import hashlib
from datetime import datetime

__authors__ = ["Ilya Semennikov"]
__date__ = "20241030"
__descripton__ = "A simple argparse example"

from datetime import datetime

parsers = argparse.ArgumentParser(
    description=__descripton__,
    epilog="Developed by {} on {}".format(
        ", ".join(__authors__), __date__)
    )

# Add Positional Arguments

parsers.add_argument("INPUT_FILE", help="Path to input files")
parsers.add_argument("OUTPUT_FILE", help="Path to output file")

#Optional Arguments

parsers.add_argument("--hash", help="Hash the files",action="store_true")
parsers.add_argument("--hash-algoritm", help="Hash algoritm to use SHA1 or/and SHA256", choices=['SHA1', 'SHA256'], default="SHA256")

parsers.add_argument("-v", "--version", "--script-version", help="Display script version information",
                     action="version", version=str(__date__))
parsers.add_argument("-l", "--log", help="Path to log file", required=True)

# Parsing and using the arguments

args = parsers.parse_args()

input_file = args.INPUT_FILE
output_file = args.OUTPUT_FILE

# logging of start parsing
with open(args.log, 'a') as log_file:
    log_file.write(f"[{datetime.now()}] Start parsing {input_file} file\n")

if args.hash:
    ha = args.hash_algoritm
    print("File hashing enabled with {} algoritm".format(ha))
    import hashlib
    hash_function = hashlib.new(ha)
    with open(input_file, 'rb') as f:
        while chunk := f.read(8192):
            hash_function.update(chunk)
    hash_value = hash_function.hexdigest()
    # hash func to output file
    with open(output_file, 'w') as output_file:
        output_file.write(f"Hash: {hash_value}\n")
    #Loggin succes ending
    log_file.write(f"[{datetime.now()}] Parsing is complit. Result of pasring in {output_file} file\n ")


if not args.log:
    print("Log file not defined. Will write to stdout")




