import toml
import sys
import re
from functools import reduce
import operator
import argparse

def get_value_from_string(dictionary, string):
    keys = string.split('.')
    return reduce(operator.getitem, keys, dictionary)

parser = argparse.ArgumentParser(
                    prog='python3 setup-env-from-toml.py',
                    description='Generate from the given toml <filename> a shell script that will setup environment variables for each key found withing <key>.',
                    epilog='Assume <key> contains a string with key=value pairs separated by spaces.\nThe variable names will be setup as <prefix>key.\nThe output is generated at stdout.\nReturns nonzero code in case of any error.')

parser.add_argument('-f', '--filename', help='Toml filename to be parsed', default='./samconfig.toml')
parser.add_argument('-k', '--key', help='Key of toml <filename> to be parsed', required=True)
parser.add_argument('-p', '--prefix', help='Prefix to be prepended to environment variable names', default='SAMCONFIG_')
args = parser.parse_args()

toml_data = toml.load(args.filename)
# print(toml_data)
params = get_value_from_string(toml_data, args.key)
if type(params) is dict:
    print("The key was not found or does not represent a valid value.", file=sys.stderr)
    sys.exit(-1)
else:
    pattern = r'(?<=\")[ ]+(?=[A-Za-z0-9])'
    res = dict( item.split("=") for item in re.split(pattern, params))
    print ("#!/bin/bash")
    for key, value in res.items():
        varname = args.prefix + key.strip()
        print('export '+varname+'='+value)
