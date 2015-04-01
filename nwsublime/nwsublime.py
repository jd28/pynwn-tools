#!/usr/bin/env python

import argparse, os, sys, re, json
import subprocess, shutil
import codecs

parser = argparse.ArgumentParser()
parser.add_argument('scripts', help='Input scripts', nargs='+')

KIND_RE = re.compile("kind:([a-zA-Z])")
SIG_RE = re.compile("signature:\((.*)\)")
ENCODING = 'cp1252' # Assume this...

SYMBOL = 0
FILENAME = 1

# The following function is from Sublime Ctags...
def resort_ctags(tag_file):
    """
    Rearrange ctags file for speed.
    Resorts (re-sort) a CTag file in order of file. This improves searching
    performance when searching tags by file as a binary search can be used.
    The algorithm works as so:
        For each line in the tag file
            Read the file name (``file_name``) the tag belongs to
            If not exists, create an empty array and store in the
                dictionary with the file name as key
            Save the line to this list
        Create a new ``[tagfile]_sorted_by_file`` file
        For each key in the sorted dictionary
            For each line in the list indicated by the key
                Split the line on tab character
                Remove the prepending ``.\`` from the ``file_name`` part of
                    the                   tag
                Join the line again and write the ``sorted_by_file`` file
    :param tag_file: The location of the tagfile to be sorted
    :returns: None
    """
    keys = {}

    with codecs.open(tag_file, encoding='utf-8', errors='replace') as file_:
        for line in file_:
            keys.setdefault(line.split('\t')[FILENAME], []).append(line)

    with codecs.open(tag_file+'_sorted_by_file', 'w', encoding='utf-8',
                     errors='replace') as file_:
        for k in sorted(keys):
            for line in keys[k]:
                split = line.split('\t')
                split[FILENAME] = split[FILENAME].lstrip('.\\')
                file_.write('\t'.join(split))

def create_tags(scripts):
    a = ['%s\ctags.exe' % os.path.dirname(os.path.realpath(__file__)),
            # Dont't need to edit these
            '--language-force=c',
            '--c-kinds=cdefgmnpstuvx',
            '--fields=fksmnSzt',
            '-f .tags']
    a.extend(scripts)
    res = subprocess.Popen(a).wait()
    resort_ctags('.tags')

vars = {}
def variable(line, holder):
    x = line.split()
    if x[0] in vars: return
    vars[x[0]] = True
    holder['completions'].append({
        'trigger': x[0],
        'contents': x[0]
    })

funcs = {}

def function(line, holder):
    match = SIG_RE.search(line)
    if not match: return
    sig = match.group(1).split(',')
    x = line.split()
    if x[0] == 'main': return
    if x[0] in funcs: return

    if x[0] not in funcs: funcs[x[0]] = []
    if x[1] not in funcs[x[0]]: funcs[x[0]].append(x[1])

    args = []
    for i, s in enumerate(sig):
        args.append('${%d:/*%s*/}' % (i+1, s.strip()))

    args = ','.join(args)
    #print(args.encode(ENCODING, errors='ignore'))

    holder['completions'].append({
        'trigger': x[0],
        'contents': '%s(%s)' % (x[0], args)
    })


DISPATCH = {
    'v': variable,
    'p': function
}

if __name__ == "__main__":
    args = parser.parse_args()
    holder = {
        'scope': 'source.nss',
        'completions': [{ 'trigger': "OBJECT_SELF", 'contents': "OBJECT_SELF"}]
    }
    print("Creating '.tags' file...")
    create_tags(args.scripts)
    print("Creating sublime completions file...")
    with open('.tags', 'r', encoding=ENCODING, errors='replace') as f:
        for line in f:
            match = KIND_RE.search(line)
            if not match: continue
            type = match.group(1)
            if type not in DISPATCH: continue
            DISPATCH[type](line, holder)

    with open('nwscript.sublime-completions', 'w') as f:
        json.dump(holder, f, ensure_ascii=True, sort_keys=True,
                  indent=4, separators=(',', ': '))

    import configparser
    config = configparser.ConfigParser()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        config.read(os.path.join(script_dir, 'nwsublime.ini'))
        out_dir = config.get('completions', 'dir')
        move = config.get('completions', 'move') == 'true'
        if os.path.isdir(out_dir):
            if move:
                shutil.move('nwscript.sublime-completions',
                             os.path.join(out_dir, 'nwscript.sublime-completions'))
            else:
                shutil.copy2('nwscript.sublime-completions',
                             os.path.join(out_dir, 'nwscript.sublime-completions'))
            print("Installed: %s" % os.path.join(out_dir, 'nwscript.sublime-completions'))
        else:
            raise IsADirectoryError('ERROR: %s is not a directory!' % out_dir)

    except Exception as e:
        print('Unable to copy completions file.')
        print(e)