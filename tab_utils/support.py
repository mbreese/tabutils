import sys,os
import gzip

class gzip_opener:
    '''
    A Python 2.6 class to handle 'with' opening of text files that may
    or may not be gzip compressed.
    '''
    def __init__(self,fname):
        self.fname = fname
    def open(self):
        return self.__enter__()
    def __enter__(self):
        if self.fname == '-':
            self.f = sys.stdin
        elif self.fname[-3:] == '.gz':
            self.f = gzip.open(os.path.expanduser(self.fname))
        else:
            self.f = open(os.path.expanduser(self.fname))
        return self.f
    def __exit__(self, type, value, traceback):
        if self.f != sys.stdin:
            self.f.close()
        return False

def filenames_to_uniq(names,new_delim='.'):
    '''
    Given a set of file names, produce a list of names consisting of the
    uniq parts of the names. This works from the end of the name.  Chunks of
    the name are split on '.' and '-'.
    
    For example:
        A.foo.bar.txt
        B.foo.bar.txt
        returns: ['A','B']
    
        AA.BB.foo.txt
        CC.foo.txt
        returns: ['AA.BB','CC']
    
    '''
    prefix = 0
    suffix = -1 

    common = True

    while common:
        for name in names[1:]:
            if name[prefix] != names[0][prefix]:
                common = False
                break
        if common:
            prefix += 1

    common = True

    while common:
        for name in names[1:]:
            if name[suffix] != names[0][suffix]:
                suffix += 1
                common = False
                break
        if common:
            suffix -= 1

    newnames = []
    for name in names:
        if suffix == 0:
            newnames.append(name[prefix:])
        else:
            newnames.append(name[prefix:suffix])

    return newnames
