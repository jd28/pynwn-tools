#!/usr/bin/env python

TDA_LOOKUP_COLUMN = {}

import re, sys, configparser
import os
from os import listdir
from os.path import isfile, join
import glob
import argparse
import shutil

from pynwn.file.twoda import TwoDA

MDL_NAME_REGEX = re.compile(r'p(\D\D)(\d_head)(\d+).[Mm][Dd][Ll]')
PLT_NAME_REGEX = re.compile(r'(.+)_head(\d+).[pP][Ll][Tt]')

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version='0.1')
parser.add_argument('-t', '--twoda', help='2da head lookup table. Default: headmodel.2da', default='headmodel.2da')
parser.add_argument('--use-nontoolset', help='Flag to se head model IDs that cannot be used in the toolset.',
                    default=False, action='store_true')
parser.add_argument('output', help='Output directory.')
parser.add_argument('input', help='Input directories', nargs='+')
args = parser.parse_args()

def load_2da_lookup(config, output, tda):
    global TDA_LOOKUP_COLUMN
    path = join(output, tda)
    if not isfile(path):
        print("Unable to load lookup table: %s" % path, file=sys.stderr)
        return None
    for opt in config.options('Lookup'):
        TDA_LOOKUP_COLUMN[opt] = config.get('Lookup', opt)
    return TwoDA(path)

def update_mdl(dir, mdl, new_id):
    m = os.path.basename(mdl).lower()
    match = MDL_NAME_REGEX.match(m)
    if not match: return
    mtype, stuff, mid = match.groups()
    new_name = 'p' + mtype + stuff + str(new_id).zfill(3) + ".mdl"

    with open(join(args.output, new_name), 'w') as new_file:
        with open(mdl, 'r') as old_file:
            print("Creating new mdl: %s -> %s" % (mdl, new_name))
            for line in old_file:
                new_file.write(line.replace('head' + str(mid).zfill(3),
                                            'head' + str(new_id).zfill(3)))
    glob_for = join(dir, 'p' + mtype +'*_head' + str(mid).zfill(3) + '.plt')
    for plt in glob.glob(glob_for):
        new_plt = 'p'+mtype+stuff+'%s.plt' % str(new_id).zfill(3)
        print("Copying PLT: %s -> %s" % (plt, new_plt))
        shutil.copy2(plt, join(args.output, new_plt))

def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def get_next_row(mtype, tda, skip):
    l = TDA_LOOKUP_COLUMN[mtype]
    col = tda.get_column_index(l) - 1
    for i, r in enumerate(tda.rows):
        if skip and (i >= 50 and i <= 99):
             continue
        test = tda.get_int(i, col)
        if test != i:
            tda.set(i, col, str(i))
            return i

    newrow = ['****'] * len(tda.rows[0])
    tda.rows.append(newrow)
    i = len(tda.rows) - 1
    tda.set(i, col, str(i))
    return i


def run(inputs, skip, output):
    converted = {}
    for dir in inputs:
        converted[dir] = {}
        for f in listdir(dir):
            p = join(dir, f)
            if not isfile(p): continue
            match = MDL_NAME_REGEX.match(f)
            if not match: continue
            mtype, _, mid = match.groups()
            nextid = get_next_row(mtype, tda, skip)
            update_mdl(dir, p, nextid)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(join(getScriptPath(), 'head_renamer.ini'))
    tda = load_2da_lookup(config, args.output, args.twoda)
    if not tda is None:
        run(args.input, not args.use_nontoolset, args.output)
        print("Updating 2da: " + join(args.output, args.twoda + '.new'))
        with open(join(args.output, args.twoda + '.new'), 'w') as f:
            f.write(str(tda))
    else:
        print("Error: Unable to load lookup table!", file=sys.stderr)
