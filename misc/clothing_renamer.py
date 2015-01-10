#!/usr/bin/env python

part_to_2da = {
    'neck': 'parts_neck.2da',
    'chest': 'parts_chest.2da',
    'belt': 'parts_belt.2da',
    'pelvis': 'parts_pelvis.2da',
    'shor': 'parts_shoulder.2da',
    'shol': 'parts_shoulder.2da',
    'bicepr': 'parts_bicep.2da',
    'bicepl': 'parts_bicep.2da',
    'forer': 'parts_forearm.2da',
    'forel': 'parts_forearm.2da',
    'handr': 'parts_hand.2da',
    'handl': 'parts_hand.2da',
    'legr': 'parts_legs.2da',
    'legl': 'parts_legs.2da',
    'shinr': 'parts_shin.2da',
    'shinl': 'parts_shin.2da',
    'footr': 'parts_foot.2da',
    'footl': 'parts_foot.2da',
}

import re
import os
from os import listdir
from os.path import isfile, join
import glob
import argparse
import shutil

from pynwn.file.twoda import TwoDA

MDL_NAME_REGEX = re.compile(r'(p\D\D\d_)(\D+)(\d+).mdl')
PLT_NAME_REGEX = re.compile(r'(.+)_(\D+)(\d+).plt')

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version='0.1')
parser.add_argument('-o', '--output', help='Output directory.', default='output')
parser.add_argument('directory', help='Input directory')
args = parser.parse_args()

if __name__ == "__main__":
    starts = {}
    twoda_old = {}
    twoda_new = {}
    converted = {}

    for f in listdir(args.directory):
        p = join(args.directory, f)
        if not isfile(p): continue

        match = MDL_NAME_REGEX.match(f)
        if not match: continue

        head, mtype, mid = match.groups()
        if not mtype in part_to_2da: continue
        mid = int(mid)

        if not mtype in starts:
            twoda_new[mtype] = TwoDA(join(args.output, part_to_2da[mtype]))
            twoda_old[mtype] = TwoDA(join(args.directory, part_to_2da[mtype]))
            starts[mtype] = len(twoda_new[mtype].rows)

        old_pat = mtype + str(mid).zfill(3)
        new_pat = mtype + str(starts[mtype]).zfill(3)

        if old_pat in converted: continue
        converted[old_pat] = True

        glob_for = join(args.directory, '*_' + mtype + str(mid).zfill(3) + '.mdl')
        for mdl in glob.glob(glob_for):
            match = MDL_NAME_REGEX.match(os.path.basename(mdl))
            head, _, _ = match.groups()
            new_name = head + new_pat + ".mdl"

            with open(join(args.output, new_name), 'w') as new_file:
                with open(mdl, 'r') as old_file:
                    print("Creating new mdl: %s -> %s" % (mdl, new_name))
                    for line in old_file:
                        new_file.write(line.replace(old_pat, new_pat))

        glob_for = join(args.directory, '*_' + mtype + str(mid).zfill(3) + '.plt')
        for plt in glob.glob(glob_for):
            match = PLT_NAME_REGEX.match(os.path.basename(plt))
            head, ptype, pid = match.groups()
            new_plt = '%s_%s%s.plt' % (head, ptype, str(starts[mtype]).zfill(3))

            print("Copying PLT: %s -> %s" % (plt, new_plt))
            shutil.copy2(plt, join(args.output, new_plt))

        twoda_new[mtype].rows.append(twoda_old[mtype].rows[mid])
        twoda_new[mtype].rows[mid][0] = str(starts[mtype])
        print(twoda_new[mtype].rows[mid][0], mid)

        print('\n')

        starts[mtype] += 1

    # Save all the twodas
    for _, v in twoda_new.items():
        with open(join(args.output, v.co.get_filename()), 'w') as f:
            f.write(str(v))
