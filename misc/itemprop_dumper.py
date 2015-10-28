#!/usr/bin/env python

# This script prints all items in a module and their properties as they'd
# appear in game.

import argparse

from pynwn import ResourceManager
from pynwn import TwoDA

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version='0.1')
parser.add_argument('--nwn', help='NWN Path.',
                    default="C:\\GOG Games\\Neverwinter Nights Diamond Edition\\")
parser.add_argument('module', help='Module.')
args = parser.parse_args()


def dump_items(resman):
    param_table = []
    cost_table = []
    subtypes = {}

    propdef = TwoDA(resman['itempropdef.2da'])
    for i in range(len(propdef.rows)):
        r = propdef.get(i, 'SubTypeResRef')
        if not len(r):
            continue
        r = r.lower() + '.2da'
        subtypes[i] = TwoDA(resman[r])

    tda = TwoDA(resman['iprp_paramtable.2da'])
    for i in range(len(tda.rows)):
        param_table.append(tda.get(i, 'TableResRef').lower() + '.2da')

    param_table = [TwoDA(resman[x]) for x in param_table]

    tda = TwoDA(resman['iprp_costtable.2da'])
    for i in range(len(tda.rows)):
        cost_table.append(tda.get(i, 'Name').lower() + '.2da')
    cost_table = [TwoDA(resman[x]) for x in cost_table]

    for i in sorted(resman.module.glob('*.uti'), key=lambda item: item.base_type):
        try:
            props = i.properties
            if not len(props):
                continue

            print("%s (%s)" % (i.get_name(0), i.resref))
            for p in props:
                if propdef.get_int(p.type, 'Name') == 0:
                    continue
                res = [resman.tlktable.get(propdef.get_int(p.type, 'Name'))]
                if p.type in subtypes:
                    strref = subtypes[p.type].get_int(p.subtype, 'Name')
                    res.append(resman.tlktable.get(strref))
                if p.cost_table > 0:
                    strref = cost_table[p.cost_table].get_int(p.cost_value, 'Name')
                    if strref > 0:
                        res.append(resman.tlktable.get(strref))
                if p.param_table != 0xFF:
                    strref = param_table[p.param_table].get_int(p.param_value, 'Name')
                    if strref > 0:
                        res.append(resman.tlktable.get(strref))

                print('  ' + ' '.join(res))
        except Exception as e:
            print("   ERROR: '%s' possibly invalid 2da" % e)


if __name__ == "__main__":
    resource_mgr = ResourceManager.from_module(args.module, False, True, args.nwn)
    dump_items(resource_mgr)
