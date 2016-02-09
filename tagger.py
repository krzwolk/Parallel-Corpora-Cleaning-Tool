# This script adds qwerty tags to the end of each line of input file

import sys


if len(sys.argv)!=3:
    print >> sys.stderr, 'Usage: %s in-file out-file'%sys.argv[0]
    sys.exit(1)


try:
    inp=open(sys.argv[1], 'r')
    out=open(sys.argv[2], 'w')
except IOError, err:
    print >> sys.stderr, err
    sys.exit(1)


line=inp.readline()
n=1
q=1
while line!='':
    line=line[:-1]
    dot=line.rfind('.')
    if dot==-1:
        print >> sys.stderr, 'Warning: No dot found on line: %d'%n
        line+='\n'
    else:
        line=line[:dot]+' qwerty%d'%q+'.\n'
        q+=1
    out.writelines(line)
    line=inp.readline()
    n+=1


inp.close()
out.close()
