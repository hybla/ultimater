# Contains functions that perform file operations
# such as reading and writing files

import os
import json

# Saves a genome (or any data) to a file
def save(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

# Reads a genome (or any data) from a file
def read(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data
