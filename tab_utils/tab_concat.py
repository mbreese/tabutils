#!/usr/bin/env python
'''
Concats multiple tab-delimited files into one text file (with a optional extra column added for the filename)
'''

import sys,os

from support import gzip_opener
from support import filenames_to_uniq

def tab_concat(fnames, add_fname=False, no_header=False, fname_label = "sample"):
    names = filenames_to_uniq([os.path.basename(x) for x in fnames])
    fobjs = []
    nextLines = []
    for fname in fnames:
        f=open(fname)
        line = f.next()
        while line[0] == '#':
            sys.stdout.write(line)
            line = f.next()
        nextLines.append(line)
        fobjs.append(f)

    if not no_header:
        if add_fname:
            cols = nextLines[0].rstrip().split('\t')
            cols.insert(0, fname_label)
            sys.stdout.write("%s\n" % "\t".join(cols))
        else:
            sys.stdout.write(nextLines[0])

        nextLines = None

    if nextLines:
        for name, line in zip(names, nextLines):
            if add_fname:
                cols = line.rstrip().split('\t')
                cols.insert(0, name)
                sys.stdout.write("%s\n" % "\t".join(cols))
            else:
                sys.stdout.write(line)
                
    for name, f in zip(names, fobjs):
        for line in f:
            if add_fname:
                cols = line.rstrip().split('\t')
                cols.insert(0, name)
                sys.stdout.write("%s\n" % "\t".join(cols))
            else:
                sys.stdout.write(line+"\n")
        f.close()
    

def usage(msg=""):
    if msg:
        print msg
    print __doc__
    print """Usage: %s {opts} filename1.tab filename2...

Options:
    -n          Add the filename as a column
    -l val      Use this label for the filename column (auto-sets -n, defaults to "file")
    -noheader   There is no header line

""" % os.path.basename(sys.argv[0])
    sys.exit(1)
    
def main(argv):
    fnames = []

    label = "file"
    add_fname = False
    no_header = False
    last = None
    for arg in argv:
        if arg in ['-h','--help']:
            usage()
        elif last == '-l':
            label = arg
            add_fname = True
            last = None
        elif arg in ['-l']:
            last = arg
        elif arg == '-n':
            add_fname = True;
        elif arg == '-noheader':
            no_header = True;
        elif os.path.exists(arg):
            fnames.append(arg)
        else:
            usage("Unknown option (or missing file): %s" % arg)

    if not fnames:
        usage("Missing input filename(s)!")

    tab_concat(fnames, add_fname, no_header, label)
    
if __name__ == '__main__':
    main(sys.argv[1:])

