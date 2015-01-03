#!/usr/bin/env python
import argparse, os, sys

from pynwn.file.erf import Erf

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version='0.1')
parser.add_argument('-o', '--output', help='Output file.', default='output.hak')
parser.add_argument('-t', '--type', help='Output type.', default='HAK')
parser.add_argument('files', help='Add files to add.', nargs='+')

if __name__ == "__main__":
    args = parser.parse_args()
    outtype = args.type.strip().upper()
    print(outtype, outtype in Erf.TYPES)
    out = Erf(outtype)
    for f in args.files:
        try:
            out.add_file(f)
        except ValueError as e:
            print("Skipping: " + str(e))

    with open(args.output, 'wb') as f:
        out.write_to(f)
