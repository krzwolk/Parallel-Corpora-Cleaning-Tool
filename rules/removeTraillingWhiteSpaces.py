import re

pat = re.compile(r'\s+')
def removeTraillingWhiteSpaces(s):
    return pat.sub(' ', s)
