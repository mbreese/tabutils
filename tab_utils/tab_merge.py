#!/usr/bin/env python
'''
Merges tab-delimited files together, combining common columns
'''
import sys,os
from support import filenames_to_uniq


class MergeException(Exception):
    pass
    
def merge_files(fnames,common_cols,uncommon_cols, noheader=False,collate=False):
    names = filenames_to_uniq([os.path.basename(x) for x in fnames])
    files = []
    for fname in fnames:
        files.append(open(fname))

    header_out = False
    for i,f in enumerate(files):
        first = True
        for line in f:
            if line[0] == '#':
                header_out = True
                sys.stdout.write('# %s %s' % (names[i],line[1:]))
                first = False
            else:
                break
        f.seek(0)

    if header_out:
        sys.stdout.write('\n')
    headers = True
    line_num = 0
    
    if noheader:
        if len(uncommon_cols) > 1:
            if not collate:
                for j in uncommon_cols:
                    for name in names:
                        sys.stdout.write('\t%s col %s' % (name,j))
            else:
                for name in names:
                    for j in uncommon_cols:
                        sys.stdout.write('\t%s col %s' % (name,j))
                
        else:
            for name in names:
                sys.stdout.write('\t%s' % (name))

        sys.stdout.write('\n')
        headers=False
        
    while True:
        lines = []
        try:
            for f in files:
                lines.append(f.next())
            line_num += 1
        except:
            break
            
        outcols = []
        common = []
        values = []
        
        for (i,line) in enumerate(lines):
            if line[0] == '#' or line.strip() == '':
                continue
                
            cols = line.strip().split('\t')
            values.append(cols)
            
            if not common:
                for j in common_cols:
                    common.append(cols[j])
            else:
                test=[]
                for j in common_cols:
                    test.append(cols[j])
                col_num=0
                for c,t in zip(common,test):
                    col_num += 1
                    if t !=c:
                        raise MergeException("Invalid common values: %s != %s (line %s, col %s)" % (t,c,line_num,col_num))

        outcols = common
        if headers:
            if collate:
                for name in names:
                    for j in uncommon_cols:
                        outcols.append('%s %s' % (name,cols[j]))
            else:
                for j in uncommon_cols:
                    for name in names:
                        outcols.append('%s %s' % (name,cols[j]))
        else:
            if collate:
                for j in uncommon_cols:
                    for cols in values:
                        if len(cols)>j:
                            outcols.append(cols[j])
                        else:
                            outcols.append('')

            else:
                for cols in values:
                    for j in uncommon_cols:
                        if len(cols)>j:
                            outcols.append(cols[j])
                        else:
                            outcols.append('')
        if outcols:
            sys.stdout.write('%s\n' % '\t'.join(outcols))

        if headers and outcols:
            headers = False

    
    for f in files:
        f.close()
        
def usage():
    print __doc__
    print """\
Usage: %s {opts} common_cols merge_cols files

common_cols and merge_cols should be a comma-separated list of column numbers.

Files should be in the same order.  New column names will be guessed 
based upon the filenames.

Options:
    -noheader    the files have no header row
    -collate     collate uncommon columns

""" % os.path.basename(sys.argv[0])
    
if __name__ == '__main__':
    
    noheader=False
    collate = False
    common = None
    uncommon = None
    files=[]
    
    for arg in sys.argv[1:]:
        if arg == '-h':
            usage()
            sys.exit(1)
        elif arg == '-noheader':
            noheader = True
        elif arg == '-collate':
            collate = True
        elif not common:
            common = [int(x)-1 for x in arg.split(',')]
        elif not uncommon:
            uncommon = [int(x)-1 for x in arg.split(',')]
        elif os.path.exists(arg):
            files.append(arg)
        else:
            usage()
            sys.exit(1)
    if not files or not common or not uncommon:
        usage()
        sys.exit(1)
        
    merge_files(files,common,uncommon,noheader,collate)
