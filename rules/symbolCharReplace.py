# encoding: utf-8

ENGLISH_SYMBOL_MAP={
    '$': 'dollar',
    '€': 'euro',
    '£': 'pound',
    '§': 'paragraph',
}
POLISH_SYMBOL_MAP={
    '$': 'dolar',
    '€': 'euro',
    '£': 'funt',
    '§': 'paragraf',
}
ENGLISH_CHAR_MAP={
    'ą': 'a',
    'ć': 'c',
    'ę': 'e',
    'ł': 'l',
    'ń': 'n',
    'ó': 'o',
    'ś': 's',
    'ż': 'z',
    'ź': 'z',
}
POLISH_CHAR_MAP={}
BOTH_CHAR_MAP=[
    ('z', 'žžȥ'),
    ('s', 'šŝşšș'),
    ('i', '¡ìíîïĩīĭįıĳǐȉȋ'),
    ('c', '¢çĉċč'),
    ('a', 'ªàáâãäåæāăǎǟǡǻǽȁȃȅȇȧ'),
    ('ss', 'ß'),
    ('e', 'èéêëēĕėěȩ'),
    ('o', 'ðòôõöōŏőǒȍȏȫȭȯȱ'),
    ('n', 'ñņňŉŋǹ'),
    ('u', 'ùúûüũūŭůűųǔǖǘǚǜȕȗ'),
    ('y', 'ýÿŷȳ'),
    ('d', 'ďđȡ'),
    ('g', 'ĝğġģǥǧǵ'),
    ('h', 'ĥĦħȟ'),
    ('j', 'Ĵĵ'),
    ('k', 'ķĸǩ'),
    ('l', 'ĺļľŀ'),
    ('r', 'ŕŗřȑȓ'),
    ('t', 'ţťŧț'),
    ('w', 'ŵ'),
    ('q', 'ǫǭ'),
]
BOTH_CHAR_MAP=[(c, unicode(group, 'utf-8', 'ignore')) for c, group in BOTH_CHAR_MAP]

def enSymbolCharReplace(line):
    return symbolCharReplace(line, ENGLISH_SYMBOL_MAP, ENGLISH_CHAR_MAP, BOTH_CHAR_MAP)


def plSymbolCharReplace(line):
    return symbolCharReplace(line, POLISH_SYMBOL_MAP, POLISH_CHAR_MAP, BOTH_CHAR_MAP)

def symbolCharReplace(line, symbolMap, charMap, multiMap):
    for symbol in symbolMap:
        line=line.replace(symbol, ' %s '%symbolMap[symbol])
    for char in charMap:
        line=line.replace(char, charMap[char])
    for main, group in multiMap:
        for c in group:
            line=line.replace(c.encode('u8'), main)
    return line
