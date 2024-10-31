from __future__ import print_function
import argparse
import hashlib
from datetime import datetime
import os

__authors__ = ["Ilya Semennikov"]
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

# Optional Arguments

parsers.add_argument("--hash", help="Hash the files", action="store_true")
parsers.add_argument("--hash-algoritm", help="Hash algoritm to use SHA1 or/and SHA256", choices=['SHA1',
                    'SHA256'], default="SHA256")
parsers.add_argument("-r", "--recursion", help="Directory to process files recursively", action="store")
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

    if args.recursion:
        # Recursion parsing in set dir
        for root, dirs, files in os.walk(args.recursion):
            for file in files:
                full_input_path = os.path.join(root, file)
                log_file.write(f"[{datetime.now()}] Parsing file {full_input_path}\n")

                if args.hash:
                    ha = args.hash_aloritm
                    print(f"File hashing enabled with {ha} algorithm for {full_input_path}")

                    # Hashing file
                    hash_func = hashlib.new(ha)
                    try:
                        with open(full_input_path, 'rb') as f:
                            while chunk := f.read(8192):
                                hash_func.update(chunk)
                        hash_value = hash_func.hexdigest()

                        # Record hash file to output file
                        with open(output_file, 'a') as out_file:  # Use "a"
                            out_file.write(f"File: {full_input_path}, Hash: {hash_value}\n")

                        # Logging is complit
                        log_file.write(
                            f"[{datetime.now()}] Parsing is complit. Result in  {output_file} file \n")
                    except Exception as e:
                        log_file.write(f"[{datetime.now()}] Error while parsing {full_input_path}: {e}\n")
                        print(f"Error while parsing {full_input_path} file: {e}")

    else:
        # Parsing file
        log_file.write(f"[{datetime.now()}] Parsing  {input_file} file \n")

        if args.hash:
            ha = args.hash_aloritm
            print(f"File hashing enabled with {ha} algorithm for {input_file}")

            # Hashing fike
            hash_func = hashlib.new(ha)
            try:
                with open(input_file, 'rb') as f:
                    while chunk := f.read(8192):
                        hash_func.update(chunk)
                hash_value = hash_func.hexdigest()

                # Hash to output file
                with open(output_file, 'w') as out_file:
                    out_file.write(f"File: {input_file}, Hash: {hash_value}\n")

                # Logging is complete
                log_file.write(f"[{datetime.now()}] Pasing is complete. Result in  {output_file} file\n")
            except Exception as e:
                log_file.write(f"[{datetime.now()}] Error while parsing {input_file}: {e}\n")
                print(f"Error while parsing {input_file}: {e}")
        else:
            log_file.write(f"[{datetime.now()}] Hash not set.\n")
