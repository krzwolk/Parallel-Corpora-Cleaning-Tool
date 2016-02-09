# This script detags qwerty tags and sync input files.
#
# 1. This script sync inp-2 to inp-1, so inp-1 is the base reference.
# 2. Tags are incremental from the first line to the last in both files.
# 3. Tags in inp-1 must be a subset of tags of inp-2.
# 4. Exactly one tag should be on each line, so empty line is not allowed.
#
# inp1 inp2 -> action
# 3    3    -> keep both lines (after removing tags)
# 5    3    -> drop lines from inp2 until finding 5. if reach end of file this is an error.
# 3    5    -> error. 3 was not found in inp-2 or inp-2 tags are not incremental.
#


import re
import sys


def error(msg):
    print >> sys.stderr, msg
    sys.exit(1)


def remove_tag(line):
    e=' ?qwerty\d+ ?'
    qwerty=re.findall(e, line, flags=re.IGNORECASE)
    if len(qwerty)!=1:
        error('error: exactly one tag should be on each line (%d found): %s'%(len(qwerty), line))
    qwerty=qwerty[0].strip().lower()
    newline=re.sub(e, '', line, flags=re.IGNORECASE)
    tagno=int(qwerty.replace('qwerty', ''))
    return newline, tagno


if len(sys.argv)!=5:
    error('Usage: %s in-file-1 in-file-2 out-file-1 out-file-2'%sys.argv[0])
try:
    inp1=open(sys.argv[1], 'r')
    inp2=open(sys.argv[2], 'r')
    out1=open(sys.argv[3], 'w')
    out2=open(sys.argv[4], 'w')
except IOError, err:
    error(err)


n1=n2=0
while True:
    line1=inp1.readline(); n1+=1
    line2=inp2.readline(); n2+=1
    if line1=='':
        break
    newline1, tagno1=remove_tag(line1)
    newline2, tagno2=remove_tag(line2)
    if tagno2>tagno1:
        error('error: reach to qwerty%d in %s but except qwerty%d'%(tagno2, inp2.name, tagno1))
    while tagno2<tagno1:
        line2=inp2.readline(); n2+=1
        if line2=='':
            error('error: reach to end of %s, but tag not found: qwerty%d'%(inp2.name, tagno1))
        newline2, tagno2=remove_tag(line2)
    out1.write(newline1)
    out2.write(newline2)

[i.close() for i in [inp1, inp2, out1, out2]]
