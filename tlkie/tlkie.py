#!/usr/bin/env python

import argparse, os, sys

from pynwn.file.tlk import Tlk
from pynwn.file.tls import TLS
from pynwn.util.helper import get_encoding

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version='0.1')
parser.add_argument('-o', '--output', help='Output TLK or TLS file.')
parser.add_argument('-l', '--language', help='TLK language.', default=0)
parser.add_argument('file', help='TLK or TLS file.', nargs='+')

args = parser.parse_args()

def load_by_ext(f, ext):
    if '.tlk' == ext:
        return Tlk(open(f, 'rb'))
    elif '.tls' == ext:
        return TLS(f)
    else:
        raise ValueError("Tlkie can only process a TLK or TLS file.")

def save_by_ext(main, ext):
    if '.tlk' == ext:
        if isinstance(main, Tlk):
            with open(args.output, 'wb') as f:
                main.write(f)
        elif isinstance(main, TLS):
            with open(args.output, 'wb') as f:
                main.write_tlk(f, args.language)
    elif '.tls' == ext:
        if isinstance(main, Tlk):
            with open(args.output, 'w', encoding=get_encoding()) as f:
                main.write_tls(f)
        elif isinstance(main, TLS):
            with open(args.output, 'w', encoding=get_encoding()) as f:
                main.write(f)


if __name__ == "__main__":
    basef = os.path.basename(args.output)
    outext = os.path.splitext(basef)[1].lower()

    if outext == '.tlk':
        main = Tlk()
    elif outext == '.tls':
        main = TLS()
    else:
        raise ValueError("Tlkie can only output a TLK or TLS file.")

    for f in args.file:
        basef = os.path.basename(f)
        ext = os.path.splitext(basef)[1]
        tl = load_by_ext(f, ext.lower())
        print("Adding: %s" % f)
        if main is None:
            main = tl
            continue
        main.inject(tl)

    print("Saving output: %s" % args.output)
    save_by_ext(main, outext)
