#!/usr/bin/env python
'''
A data aware tab-delimited file viewer

Works by reading in the first few lines to determine the appropriate widths 
for each of the columns.  It will then display the data with the appropriate 
spacing to keep columns together.  If a future cell is larger than the 
predetermined size, it is truncated.

This can then be fed into something like 'less' for paging
'''

import sys,os,math
from support import gzip_opener

def tab_view(fname,preview_lines=100):
    colsizes = []
    coltypes = []
    preview_buf = []
    prev_count = 0
    inpreview = True
    try:
        with gzip_opener(fname) as f:
            for line in f:
                if inpreview and line[0] == '#':
                    preview_buf.append(line)
                else:
                    if inpreview:
                        cols = line.rstrip().split('\t')
                    
                        for i,col in enumerate(cols):
                            if len(colsizes) <= i:
                                colsizes.append(len(col))
                                coltypes.append('i')
                            elif len(col) > colsizes[i]:
                                colsizes[i] = len(col)
                            try:
                                v = int(col)
                            except:
                                coltypes[i] = 't'

                        preview_buf.append(line)
                        prev_count += 1
                        if prev_count >= preview_lines:
                            colsizes = [ int(math.ceil(x * 1.2)) for x in colsizes ]
                            for preview in preview_buf:
                                _write_cols(preview,colsizes,coltypes)
                            preview_buf = None
                            inpreview=False
                    else:
                        _write_cols(line,colsizes,coltypes)

        if preview_buf:
            colsizes = [ int(math.ceil(x * 1.2)) for x in colsizes ]
            for preview in preview_buf:
                _write_cols(preview,colsizes,coltypes)
    except KeyboardInterrupt:
        print ""
        pass
    except IOError:
        print ""
        pass
    

def _write_cols(line,colsizes,coltypes):
    cols = line.rstrip().split('\t')

    while len(cols) < len(colsizes):
        cols.append('')
        
    for i,col in enumerate(cols):
        if i>=len(colsizes):
            val = '%s' % col # for headers w/o values
        elif len(col) > colsizes[i]:  
            # if too big, show as much as possible, and indicate the 
            # truncation with '$'
            val = '%s$' % col[:colsizes[i]-1]
        elif coltypes[i] == 'i':
            # numbers right justified
            val = col.rjust(colsizes[i])
        else:
            # text left justified
            val = col.ljust(colsizes[i])
        
        sys.stdout.write(val)
        if i < (len(cols) - 1):
            sys.stdout.write(' | ')
    sys.stdout.write('\n')
    
def usage():
    print __doc__
    print """Usage: %s {-l lines} filename.tab

Options:
-l lines  The number of lines to read in to estimate the size of a column.
          [default 100]

""" % os.path.basename(sys.argv[0])
    sys.exit(1)
    
def main(argv):
    fname = '-'
    lines = 100
    
    last = None
    for arg in argv:
        if arg in ['-h','--help']:
            usage()
        elif last == '-l':
            lines = int(arg)
            last = None
        elif arg == '-l':
            last = arg
        elif arg == '-':
            fname = '-'
        elif os.path.exists(arg):
            fname = arg
        
    tab_view(fname,lines)
    
if __name__ == '__main__':
    main(sys.argv[1:])