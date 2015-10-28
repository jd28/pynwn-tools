#!/usr/bin/env python

import argparse

from pynwn import ResourceManager
from pynwn import TwoDA

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version='0.1')
parser.add_argument('--nwn', help='NWN Path.',
                    default="C:\\GOG Games\\Neverwinter Nights Diamond Edition\\")
parser.add_argument('module', help='Module.')
args = parser.parse_args()

if __name__ == "__main__":
    resman = ResourceManager.from_module(args.module, False, True, args.nwn)
    feat = TwoDA(resman['feat.2da'])
    res = {}
    for tda in [TwoDA(t) for t in resman.glob('cls_feat_*.2da')]:
        print(tda.co.resref, tda.co.io)
        d = {}
        for i in range(len(tda.rows)):
            feat_type = tda.get_int(i, 'List')
            ls = ""
            if feat_type == 0:
                ls = 'General Feat Only'
            elif feat_type == 1:
                ls = 'General or Bonus Feat'
            elif feat_type == 2:
                ls = 'Bonus Feat Only'
            elif feat_type == 3:
                ls = 'Class Granted Feat'

            strref = feat.get_int(tda.get_int(i, 'FeatIndex'), 'FEAT')
            name = resman.tlktable.get(strref)
            if feat_type == 3:
                name = "%s (%s)" % (name, tda.get(i, 'GrantedOnLevel'))

            if ls in d:
                d[ls].append(name)
            else:
                d[ls] = [name]

        res[tda.co.resref] = d

    for k, v in res.items():
        print(k)
        for ls in sorted(v.keys()):
            if not len(v[ls]):
                continue
            print("  * %s:\n    * " % ls, end="")
            print('\n    * '.join(sorted(v[ls])))
