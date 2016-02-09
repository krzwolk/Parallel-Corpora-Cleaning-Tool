# encoding: utf-8
from config import *

POLISH_UPPER=unicode('AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŻŹ', 'utf-8')
POLISH_LOWER=unicode('aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź', 'utf-8')
ENGLISH_UPPER=unicode('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'utf-8')
ENGLISH_LOWER=unicode('abcdefghijklmnopqrstuvwxyz', 'utf-8')

upper2lowerMap=dict([(c, (POLISH_LOWER+ENGLISH_LOWER)[i]) for i, c in enumerate(POLISH_UPPER+ENGLISH_UPPER)])
lower2upperMap=dict([(c, (POLISH_UPPER+ENGLISH_UPPER)[i]) for i, c in enumerate(POLISH_LOWER+ENGLISH_LOWER)])

def isUpper(c): return c in upper2lowerMap
def capitalizedLower(s):
    s=unicode(s, 'utf-8')
    s=s.strip()
    if len(s)==0: return ''
    ret=lower2upperMap[s[0]] if s[0] in lower2upperMap else s[0]
    for c in s[1:]:
        if c in upper2lowerMap: ret+=upper2lowerMap[c]
        else: ret+=c
    return ret.encode('u8')
if __name__=='__main__':
    print(capitalizedLower('Ocean jest skomplikowany jak koń. '))