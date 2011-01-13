#!/usr/bin/env python
'''
Filters a tab-delmited file based upon configurable critera
'''

import sys,os,gzip
from support import gzip_opener

def usage():
    print __doc__
    print """\
Usage: %s file.txt {criteria}

Where criteria is a set of operations in the form of:
col# operation value

Eg: 
1 eq foo
Column 1 (first column) is equal to 'foo'

1 eq foo 2 lt 3
Column 1 (first column) is equal to 'foo' and column 2 is less than 3

Valid operation:
eq
ne
lt
lte
gt
gte
contains

All comment lines are printed as-is.
""" % os.path.basename(sys.argv[0])

class Criteria(object):
    @staticmethod
    def parse_args(args):
        c = Criteria()
        for i in xrange(0,len(args),3):
            if args[i+1] in Criteria.__dict__:
                c.add_criterion(int(args[i])-1,args[i+1],args[i+2])
            else:
                print "Unknown filter function: %s" % args[i+1]
                sys.exit(1)
        
        return c
        
        
    def __init__(self,criteria=None):
        if criteria:
            self.criteria = criteria
        else:
            self.criteria = []
    
    def add_criterion(self,col,func,arg):
        self.criteria.append((col,func,arg))
        
    def filter(self,cols):
        for col,func,arg in self.criteria:
            try:
                if not Criteria.__dict__[func](self,cols[col],arg):
                    return False
            except Exception, e:
                return False
        return True
    
    def eq(self,val,arg):
        return val == arg
    def contains(self,val,arg):
        return arg in val
    def ne(self,val,arg):
        return val != arg
    def lt(self,val,arg):
        return float(val) < float(arg)
    def lte(self,val,arg):
        return float(val) <= float(arg)
    def gt(self,val,arg):
        return float(val) > float(arg)
    def gte(self,val,arg):
        return float(val) >= float(arg)

def filter_file(fname,criteria):
    with gzip_opener(fname) as f:
        for line in f:
            if line[0] == '#':
                sys.stdout.write(line)
                continue
                
            cols = line.strip().split()
            good = True
            if criteria.filter(cols):
                sys.stdout.write(line)
                
if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        usage()
        sys.exit(1)
    criteria = Criteria.parse_args(sys.argv[2:])
    filter_file(sys.argv[1],criteria)
