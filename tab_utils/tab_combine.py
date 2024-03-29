#!/usr/bin/env python
'''
Combines multiple tab-delimited files into one XLSX file
'''

import sys,os
import xlsxwriter

from support import gzip_opener

def tab_combine(outfile, fnames ,delim='\t', exclude_comments=False, nourl=False):
    workbook = xlsxwriter.Workbook(outfile, {'strings_to_numbers': True,  'strings_to_urls': not nourl })

    for fname in fnames:
        sys.stderr.write(fname.rstrip(".gz").rstrip(".txt"))
        sys.stderr.write("... ")
        worksheet = workbook.add_worksheet(os.path.basename(fname).rstrip(".gz").rstrip(".txt")[:31])
        f = gzip_opener(fname).open()
        row = 0
        for line in f:
            if exclude_comments and line[0] == '#':
                continue
            line = line.decode('utf-8')
            cols = line.rstrip().split(delim)
            for col, val in enumerate(cols):
                worksheet.write(row, col, val)
            row += 1
        sys.stderr.write("done\n")
        f.close()

    workbook.close()



def usage(msg=""):
    if msg:
        print msg
    print __doc__
    print """Usage: %s {opts} outfile.xlsx filename1.tab filename2...

Options:
    --no-comments   Don't inclue comments in the worksheets
    --no-urls       Don't convert URLs to hyperlinks
    -f              Force overwriting the output file.
    -d delim        Use this (opposed to a tab) for the delimiter

""" % os.path.basename(sys.argv[0])
    sys.exit(1)
    
def main(argv):
    outfile = None
    fnames = []

    delim = '\t'
    force = False
    exclude_comments = False
    nourl = False
    last = None
    for arg in argv:
        if arg in ['-h','--help']:
            usage()
        elif last == '-d':
            delim = arg
            last = None
        elif arg in ['-d']:
            last = arg
        elif arg == '--no-urls':
            nourl = True;
        elif arg == '--no-comments':
            exclude_comments = True;
        elif arg == '-f':
            force = True;
        elif not outfile:
            outfile = arg
        elif os.path.exists(arg):
            fnames.append(arg)

    if outfile and os.path.exists(outfile) and not force:
        usage("%s exists! If you want to overwrite this file, use the -f (force) option!" % outfile)

    if not outfile or not fnames:
        usage("Missing output file or input filename(s)!")

    tab_combine(outfile, fnames, delim, exclude_comments, nourl)
    
if __name__ == '__main__':
    main(sys.argv[1:])

