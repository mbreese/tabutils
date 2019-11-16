#!/usr/bin/env python
'''
Concats multiple tab-delimited files into one text file (with a optional extra column added for the filename)
If a file has missing columns, they will be blank
If a file has extra columns, the will be silently removed

If there is no header, this goes out the window :)

'''

import sys,os,gzip

from support import gzip_opener
from support import filenames_to_uniq

def tab_concat(fnames, add_fname=False, no_header=False, fname_label = "sample", pre='', names=None):
    if not names:
        names = filenames_to_uniq([os.path.basename(x) for x in fnames])
    fobjs = []
    nextLines = []
    headerCols = None

    writtenLines = set()
    for fname in fnames:
        if fname[-3:] == '.gz':
            f=gzip.open(fname)
        elif fname == '-':
            f = sys.stdin
        else:
            f=open(fname)
        line = f.next()
        while line[0] == '#':
            if not line in writtenLines:
                writtenLines.add(line)
                sys.stdout.write(line)
            line = f.next()
        nextLines.append(line)
        fobjs.append(f)

    headerCols = [] # list of lists; each list is the out-col index for the columns in this file
    if not no_header:
        # there is a header...

        headerNames = None # the main output header
        # read the column headers...
        for line in nextLines:
            cols = line.rstrip('\n').split('\t')
            if not headerNames:
                # first file, these are the headers we will use (and the order)
                headerNames = cols
                headerCols.append([])
                for idx,col in enumerate(cols):
                    headerCols[0].append(idx)
            else:
                # look up the header column names
                lookup=[-1,] * len(cols)
                for i,c1 in enumerate(cols):
                    for j, c2 in enumerate(headerNames):
                        if c1 == c2:
                            lookup[i] = j
                headerCols.append(lookup)

        if add_fname:
            cols = nextLines[0].rstrip('\n').split('\t')
            cols.insert(0, fname_label)
            sys.stdout.write("%s\n" % "\t".join(cols))
        else:
            sys.stdout.write(nextLines[0])

        nextLines = None

    if nextLines:
        # there is no header, so just output cols
        for name, line in zip(names, nextLines):
            cols = line.rstrip('\n').split('\t')
            headerCols.append(list(range(0,len(cols))))
#            if add_fname:
#                cols.insert(0, '%s%s' % (pre, name))
#            sys.stdout.write("%s\n" % "\t".join(cols))
               
    for i, (name, f) in enumerate(zip(names, fobjs)):
        if nextLines and nextLines[i]:
            cols = nextLines[i].rstrip('\n').split('\t')
            outcols = ['',] * len(headerCols[0])
            for j, val in enumerate(headerCols[i]):
                # j is the column in the file
                # val is the target column

                if val > -1 and len(cols) > j:
                    outcols[val] = cols[j]

            if add_fname:
                outcols.insert(0, '%s%s' %  (pre, name))

            sys.stdout.write("%s\n" % "\t".join(outcols))


#        print headerCols[i]
        for line in f:
            cols = line.rstrip('\n').split('\t')
            outcols = ['',] * len(headerCols[0])

            # we have headers, so let's match them up...
            for j, val in enumerate(headerCols[i]):
                # j is the column in the file
                # val is the target column

                if val > -1 and len(cols) > j:
                    outcols[val] = cols[j]

            if add_fname:
                outcols.insert(0, '%s%s' %  (pre, name))

            sys.stdout.write("%s\n" % "\t".join(outcols))

        if f != sys.stdin:
            f.close()
    

def usage(msg=""):
    if msg:
        print msg
    print __doc__
    print """Usage: %s {opts} filename1.tab filename2...

Options:
    -n                     Add the filename as a column (only the unique part of the name is used)
    -names val,val,...     Use these values instead of the filename (comma-separated)
    -l val                 Use this label for the filename column in the header (auto-sets -n, defaults to "file")
    -pre val               Add this prefix to the auto-extracted label (based on filename)
    -noheader              There is no header line

""" % os.path.basename(sys.argv[0])
    sys.exit(1)
    
def main(argv):
    fnames = []

    names = None

    label = "file"
    add_fname = False
    no_header = False
    pre = ""

    last = None
    for arg in argv:
        if arg in ['-h','--help']:
            usage()
        elif last == '-l':
            label = arg
            add_fname = True
            last = None
        elif last == '-names':
            names = arg.split(',')
            last = None
        elif last == '-pre':
            pre = arg
            add_fname = True
            last = None
        elif arg in ['-l', '-pre','-names']:
            last = arg
        elif arg == '-n':
            add_fname = True;
        elif arg == '-noheader':
            no_header = True;
        elif os.path.exists(arg) or arg == '-':
            fnames.append(arg)
        else:
            usage("Unknown option (or missing file): %s" % arg)

    if not fnames:
        usage("Missing input filename(s)!")
    if names and len(names) != len(fnames):
        usage("-names should have the same number of values as the number of filenames!")

    tab_concat(fnames, add_fname, no_header, label, pre, names)
    
if __name__ == '__main__':
    main(sys.argv[1:])

