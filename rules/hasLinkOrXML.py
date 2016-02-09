LINK_PATTERNS=['http://', 'https://', 'ftp://', 'www.']

def hasLinkOrXML(s):
    for pattern in LINK_PATTERNS:
        if s.find(pattern)>-1: return True
    if s.find('<')>-1 and s.find('>', s.find('<'))>-1: return True
    return False
