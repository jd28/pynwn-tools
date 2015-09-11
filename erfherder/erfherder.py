#!/usr/bin/env python
import argparse, os, sys, fnmatch, hashlib, pprint

from pynwn.file.erf import Erf

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version='0.2')
subparsers = parser.add_subparsers(description='erfherder commands', dest='sub_commands')

# pack
parser_pack = subparsers.add_parser('pack', description='Pack files and directories into an ERF file.')
parser_pack.add_argument('--exclude', help='Exclude files, directories, patterns.', action='append')
parser_pack.add_argument('output', help='Output ERF. Extension determines ERF type.')
parser_pack.add_argument('input', help='Add files/directories to add.', nargs='+')

# dump
parser_pack = subparsers.add_parser('dump', description='Dump files from an ERF.')
parser_pack.add_argument('-p', '--pattern', help='Unix wildcard pattern.')
parser_pack.add_argument('output', help='Output directory.')
parser_pack.add_argument('input', help='Source ERFs.', nargs='+')
parser_pack.add_argument('--subdir', help='Flag to create subdirectories for each ERF in OUTPUT directory.',
                         default=False, action='store_true')
# ls
parser_pack = subparsers.add_parser('ls', description='List files from an ERF.')
parser_pack.add_argument('input', help='Source ERF.', nargs='+')

# rm
parser_pack = subparsers.add_parser('rm', description='Remove files from an ERF.')
parser_pack.add_argument('input', help='Source ERF.')
parser_pack.add_argument('pattern', help='File name or quoted unix file pattern.')
parser_pack.add_argument('-o', '--output', help='Output ERF. Optional.')

# hash
parser_pack = subparsers.add_parser('hash', description='Generate hashes.')
parser_pack.add_argument('input', help='Source ERF.')
parser_pack.add_argument('-t', '--type', help='Hash type. (sha1, md5, sha256).  Default: sha1', default='sha1')

# dupes
parser_pack = subparsers.add_parser('dupes', description='Find duplicate files by sha1')
parser_pack.add_argument('-p', '--pattern', help='Unix wildcard pattern.')
parser_pack.add_argument('input', help='Input ERF files.', nargs='+')

def rm(source, pat, out):
    if out is None: out = source
    erf = Erf.from_file(source)
    dele = [co.get_filename() for co in erf.content
             if fnmatch.fnmatch(co.get_filename(), pat)]
    for fn in dele:
        print("Removing: '%s'." % fn, file=sys.stdout)
        erf.remove(fn)
    print("Saving: '%s'." % out, file=sys.stdout)
    erf.write_to(out)


def dump(sources, dest, pat, subdir):
    for source in sources:
        base = os.path.basename(source)
        base = os.path.splitext(base)[0]
        if not os.path.isdir(dest):
            os.mkdir(dest)
        elif not os.path.isfile(source):
            print("Error: Unable to locate '%s'." % source, file=sys.stderr)
            continue

        try:
            out = Erf.from_file(source)
            ndest = os.path.join(dest, base) if subdir else dest
            if not os.path.isdir(ndest):
                os.mkdir(ndest)
            for co in out.content:
                if not pat or fnmatch.fnmatch(co.get_filename(), pat):
                    co.write_to(os.path.join(ndest, co.get_filename()))

        except ValueError as e:
            print("Error: Unable to open %s: %s." % str(e), file=sys.stderr)

def pack(fout, fin, excludes):
    def check_excluded(path):
        ignore = False
        if excludes:
            for ex in excludes:
                if fnmatch.fnmatch(path, ex):
                    print("Ignoring: " + path)
                    ignore = True

        return ignore

    def add_file(erf, file):
        if os.path.isfile(file):
            if check_excluded(file): return
            try:
                out.add_file(file)
            except ValueError as e:
                print("Skipping: " + str(e))
        else:
            print("Error: Unable to add: %s is not a file." % f, file=sys.stderr)

    ext = os.path.splitext(fout)[1][1:].upper()
    if not ext in Erf.TYPES:
        print("Error: Unsupported output file extension: %s." % ext, file=sys.stderr)
        return

    if os.path.isfile(fout):
        out = Erf.from_file(fout)
    else:
        out = Erf(ext)

    for f in fin:
        if os.path.isdir(f):
            for root, _, files in os.walk(f):
                if check_excluded(root): continue

                for file in files:
                    add_file(out, os.path.join(root, file))
        else:
            add_file(out, f)

    out.write_to(args.output)

def ls(erfs):
    for erf in erfs:
        e = Erf.from_file(erf)
        res = []
        total = 0
        for co in e.content:
            res.append((co.get_filename(), co.size))
            total += co.size

        res = sorted(res, key=lambda c: c[0])
        try:
            sys.stdout.write('%s:\n' % erf)
            sys.stdout.write('files: %d, size: %d\n' % (len(res), total))
            for r in res:
                sys.stdout.write('%-20s %d\n' % r)
        except OSError:
            pass

        sys.stdout.write('\n')

def hsh(erf, type):
    type = type.lower()
    if not type in ['sha1', 'md5', 'sha256']:
        print("Error: Invalid hash type: %s!" % type)
        return

    e = Erf.from_file(erf)
    res = []
    for co in e.content:
        if type == 'md5':
            h = hashlib.md5()
        elif type == 'sha256':
            h = hashlib.sha256()
        elif type == 'sha1':
            h = hashlib.sha1()
        else:
            assert(False)
        h.update(co.get())
        res.append((co.get_filename(), h.hexdigest()))

    res = sorted(res, key=lambda c: c[0])
    try:
        sys.stdout.write('total %d\n' % len(res))
        for r in res:
            sys.stdout.write('%-20s %s\n' % r)
    except OSError:
        pass


def dupes(erfs):
    pp = pprint.PrettyPrinter(indent=2)
    shas = {}
    for erf in erfs:
        e = Erf.from_file(erf)
        for co in e.content:
            m = hashlib.sha1()
            m.update(co.get())
            d = m.hexdigest()
            t = (erf, co.get_filename(), co.size)
            if d in shas:
                shas[d].append(t)
            else:
                shas[d] = [t]


    size = 0
    for k, v in shas.items():
        if len(v) > 1:
            size += v[0][2] * (len(v) - 1)
            pp.pprint(v)
    print("Wasted space: %d in bytes." % size)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.argv.append('--help')

    args = parser.parse_args()
    if args.sub_commands == 'pack':
        pack(args.output, args.input, args.exclude)
    elif args.sub_commands == 'dump':
        dump(args.input, args.output, args.pattern, args.subdir)
    elif args.sub_commands == 'dupes':
        dupes(args.input)
    elif args.sub_commands == 'ls':
        ls(args.input)
    elif args.sub_commands == 'hash':
        hsh(args.input, args.type)
    elif args.sub_commands == 'rm':
        rm(args.input, args.pattern, args.output)
    elif args.sub_commands == "help":
        if not args.command:
            args.parse_args(['--help'])
        else:
            args.parse_args([parsed.command, '--help'])
