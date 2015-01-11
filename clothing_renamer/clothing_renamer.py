#!/usr/bin/env python

part_to_2da = {
    'neck': 'parts_neck.2da',
    'chest': 'parts_chest.2da',
    'belt': 'parts_belt.2da',
    'pelvis': 'parts_pelvis.2da',
    'sho': 'parts_shoulder.2da',
    'sho': 'parts_shoulder.2da',
    'bicep': 'parts_bicep.2da',
    'bicep': 'parts_bicep.2da',
    'fore': 'parts_forearm.2da',
    'fore': 'parts_forearm.2da',
    'hand': 'parts_hand.2da',
    'hand': 'parts_hand.2da',
    'leg': 'parts_legs.2da',
    'leg': 'parts_legs.2da',
    'shin': 'parts_shin.2da',
    'shin': 'parts_shin.2da',
    'foot': 'parts_foot.2da',
    'foot': 'parts_foot.2da',
}

import re
import os
from os import listdir
from os.path import isfile, join
import glob
import argparse
import shutil

from pynwn.file.twoda import TwoDA

MDL_NAME_REGEX = re.compile(r'(p\D\D\d_)(\D+)(\d+).[Mm][Dd][Ll]')
MDL_NAMERL_REGEX = re.compile(r'(p\D\D\d_)(\D+)([rlRL])(\d+).[Mm][Dd][Ll]')
PLT_NAME_REGEX = re.compile(r'(.+)_(\D+)(\d+).[pP][Ll][Tt]')
PLT_NAMERL_REGEX = re.compile(r'(.+)_(\D+)([rlRL])(\d+).[pP][Ll][Tt]')

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version='0.1')
parser.add_argument('output', help='Output directory.')
parser.add_argument('input', help='Input directory', nargs='+')
args = parser.parse_args()


def update_mdl(mdl, new_id):
    m = os.path.basename(mdl).lower()
    match = MDL_NAMERL_REGEX.match(m)
    if not match:
        match = MDL_NAME_REGEX.match(m)
        if not match: return
        head, mtype, mid = match.groups()
        rl = ''
    else:
        head, mtype, rl, mid = match.groups()
    new_name = head + mtype + rl + str(new_id).zfill(3) + ".mdl"

    with open(join(args.output, new_name), 'w') as new_file:
        with open(mdl, 'r') as old_file:
            print("Creating new mdl: %s -> %s" % (mdl, new_name))
            for line in old_file:
                new_file.write(line.replace(mtype + rl  + str(mid).zfill(3),
                                            mtype + rl  + str(new_id).zfill(3)))


if __name__ == "__main__":
    starts = {}
    twoda_old = {}
    twoda_new = {}
    converted = {}
    olded     = {}
    newed     = {}

    def set_starts(type, row):
        if type in ['footr', 'footl']:
            starts['footr'] = row
            starts['footl'] = row
        elif type in ['legr', 'legl']:
            starts['legr'] = row
            starts['legl'] = row
        elif type in ['shinr', 'shinl']:
            starts['shinr'] = row
            starts['shinl'] = row
        elif type in ['handl', 'handr']:
            starts['handl'] = row
            starts['handr'] = row
        elif type in ['shor', 'shol']:
            starts['shor'] = row
            starts['shol'] = row
        elif type in ['bicepr', 'bicepl']:
            starts['bicepr'] = row
            starts['bicepl'] = row
        elif type in ['forer', 'forel']:
            starts['forer'] = row
            starts['forel'] = row
        else:
            starts[type] = row

    for dir in args.input:
        twoda_old[dir] = {}
        olded[dir] = {}
        converted[dir] = {}
        for f in listdir(dir):
            p = join(dir, f)
            if not isfile(p): continue

            match = MDL_NAMERL_REGEX.match(f)
            if not match:
                match = MDL_NAME_REGEX.match(f)
                if not match:
                    continue
                head, mtype, mid = match.groups()
                rl = ''
            else:
                head, mtype, rl, mid = match.groups()

            if not mtype in part_to_2da: continue
            mid = int(mid)

            if not mtype in twoda_new:
                if not part_to_2da[mtype] in newed:
                    newed[part_to_2da[mtype]] = TwoDA(join(args.output, part_to_2da[mtype]))
                twoda_new[mtype] = newed[part_to_2da[mtype]]

            if not mtype in starts:
                set_starts(mtype, len(twoda_new[mtype].rows))

            if not mtype in twoda_old[dir]:
                if not part_to_2da[mtype] in olded:
                    olded[dir][part_to_2da[mtype]] = TwoDA(join(dir, part_to_2da[mtype]))
                twoda_old[dir][mtype] = olded[dir][part_to_2da[mtype]]

            old_pat = mtype + str(mid).zfill(3)
            new_pat = mtype + str(starts[mtype]).zfill(3)

            if old_pat in converted[dir]: continue
            converted[dir][old_pat] = True

            if len(rl):
                glob_for = join(dir, '*_' + mtype + '[rlRL]' + str(mid).zfill(3) + '.mdl')
            else:
                glob_for = join(dir, '*_' + mtype + str(mid).zfill(3) + '.mdl')
            for mdl in glob.glob(glob_for):
                update_mdl(mdl, starts[mtype])

            if len(rl):
                glob_for = join(dir, '*_' + mtype + '[rlRL]' + str(mid).zfill(3) + '.plt')
            else:
                glob_for = join(dir, '*_' + mtype + str(mid).zfill(3) + '.plt')
            for plt in glob.glob(glob_for):
                match = PLT_NAME_REGEX.match(os.path.basename(plt).lower())
                if not match:
                    print("Error: " + os.path.basename(plt))
                head, ptype, pid = match.groups()
                new_plt = '%s_%s%s.plt' % (head, ptype, str(starts[mtype]).zfill(3))

                print("Copying PLT: %s -> %s" % (plt, new_plt))
                shutil.copy2(plt, join(args.output, new_plt))

            twoda_new[mtype].rows.append(twoda_old[dir][mtype].rows[mid])
            twoda_new[mtype].rows[mid][0] = str(starts[mtype])
            print('\n')

            starts[mtype] += 1

    # Save all the twodas
    for _, v in twoda_new.items():
        with open(join(args.output, v.co.get_filename()), 'w') as f:
            f.write(str(v))
