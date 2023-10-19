"""
A data management plan tool to take stock of all files in a directory
tree.

Douglas McCulloch, October 2023
"""

import json
import os
import sys
import hashlib

# Setup parameters
ignore_hidden = 1
conda_override = 0  # sort of pointless because PATH varies in conda env's
json_filename = "DMP_list_test.json"

if os.environ["PATH"].find("Anaconda") > -1 and not conda_override:
    dir_name = os.getcwd()
else:  # assume we have executed from command line (input path)
    dir_name = str(sys.argv[1])


# Hash files and add to dict
print("Hashing", dir_name, end="...")
file_d = { }

def hash_dir(cwd: str):
    file_list = os.listdir(cwd)
    file_d[cwd] = { }
    
    for file in file_list:
        if file[0] == '.' and ignore_hidden:
            continue
        
        filepath = cwd + os.sep + file
        
        if os.path.isdir(filepath):
            hash_dir(filepath)
            continue
        
        with open(filepath, "rb") as f:
            file_d[cwd][file] = hashlib.file_digest(f, "md5").hexdigest()
    
hash_dir(dir_name)

print("done")


# Dump JSON to file
print("Writing to file", json_filename, end="...")
try:
    json_f = open(json_filename, "wt")
except FileNotFoundError:
    json_f = open(json_filename, "xt")

json.dump(file_d, json_f)

print("done")

# Clean up
json_f.close()
