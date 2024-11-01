from __future__ import print_function
import argparse
import hashlib
from datetime import datetime
import os

__authors__ = ["Ilya Semennikov"]
__date__ = "20241030"
__description__ = "A simple argparse example"

parsers = argparse.ArgumentParser(
    description=__description__,
    epilog="Developed by {} on {}".format(
        ", ".join(__authors__), __date__)
)

# Add Positional Arguments
parsers.add_argument("INPUT_FILE", help="Path to input file or directory")
parsers.add_argument("OUTPUT_FILE", help="Path to output file")

# Optional Arguments
parsers.add_argument("--hash", help="Hash the files", action="store_true")
parsers.add_argument("--hash-algoritm", help="Hash algorithm to use: SHA1 or SHA256", choices=['SHA1', 'SHA256'],
                     default="SHA256")
parsers.add_argument("-l", "--log", help="Path to log file", required=True)

# Parsing and using the arguments
args = parsers.parse_args()

input_path = args.INPUT_FILE
output_file = args.OUTPUT_FILE

# Logging the start of parsing
with open(args.log, 'a') as log_file:
    if os.path.isdir(input_path):
        log_file.write(f"[{datetime.now()}] Start parsing directory {input_path}\n")

        # Recursively process files in the set directory
        for root, dirs, files in os.walk(input_path):
            for file in files:
                full_input_path = os.path.join(root, file)
                log_file.write(f"[{datetime.now()}] Parsing the file {full_input_path}\n")

                if args.hash:
                    ha = args.hash_algoritm
                    print(f"File hashing enabled with {ha} algorithm for {full_input_path}")

                    # Hashing the file
                    hash_func = hashlib.new(ha)
                    try:
                        with open(full_input_path, 'rb') as f:
                            while chunk := f.read(8192):
                                hash_func.update(chunk)
                        hash_value = hash_func.hexdigest()

                        # Write hash sum to output file
                        with open(output_file, 'a') as out_file:  # Use 'a' for adding
                            out_file.write(f"Hash: {hash_value}\n")

                        # Logging successful completion
                        log_file.write(
                            f"[{datetime.now()}] Processing completed successfully. The result is written to {output_file} file\n")
                    except Exception as e:
                        log_file.write(f"[{datetime.now()}] Erro parsing {full_input_path} file: {e}\n")
                        print(f"Error parsing  {full_input_path} file: {e}")
    else:
        # Parsing one file
        log_file.write(f"[{datetime.now()}] Start parsing {input_path} file\n")

        if args.hash:
            ha = args.hash_algoritm
            print(f"File hashing enabled with {ha} algorithm for {input_path}")

            # Hashing the file
            hash_func = hashlib.new(ha)
            try:
                with open(input_path, 'rb') as f:
                    while chunk := f.read(8192):
                        hash_func.update(chunk)
                hash_value = hash_func.hexdigest()

                # Write hash sum to output file
                with open(output_file, 'w') as out_file:
                    out_file.write(f"Hash: {hash_value}\n")

                # Logging successful completion
                log_file.write(f"[{datetime.now()}] Processing completed successfully. The result is written to {output_file} file\n")
            except Exception as e:
                log_file.write(f"[{datetime.now()}] Error parsing {input_path} file: {e}\n")
                print(f"Erros parsing {input_path} file: {e}")
        else:
            log_file.write(f"[{datetime.now()}] Hasing not set.\n")
