# File Hashing Script

## Description
This Python script allows users to compute the hash values of files within a specified directory or for individual 
files. It supports both SHA1 and SHA256 hashing algorithms and can process files recursively in a given directory. 
The results, including the hash values, are saved to an output file, and detailed logs of the operations are maintained
in a specified log file.

## Usage
To run the script, use the following command:

```bash
python just_arguments.py <INPUT_FILE_OR_DIRECTORY> <OUTPUT_FILE> --hash --hash-algoritm <ALGORITHM> -l <LOG_FILE>
```
## Future Improvements

- Explore additional argparse functionality: Implement the argparse.FileType object to accept file objects directly as
input, enhancing usability
- Argument Defaults Help Formatter: Utilize the argparse.ArgumentDefaultsHelpFormatter class to display default values
for optional arguments, providing users with clear information on what will be used if no specific
values are provided

- Error Handling Enhancements: Improve error handling to provide more informative messages and suggestions for common 
issues

- Output Formatting Options: Allow users to choose different output formats for the results, such as JSON or CSV, 
for easier integration with other tools