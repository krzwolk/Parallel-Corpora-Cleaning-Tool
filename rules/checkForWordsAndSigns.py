# encoding: utf-8
from capitalizedLower import *

SCAN_ENGLISH_WORDS=[]
SCAN_ENGLISH_SIGNS=['á', 'à', 'â', 'ä', 'æ', 'ã', 'å', 'ā', 'é', 'è', 'ê', 'ë', 'ė', 'ē', 'ç', 'č', 'ê', 'ô', 'ò', 'õ', 'œ', 'ö', 'ß', 'ü']
SCAN_POLISH_WORDS=['that', 'the', 'vote', 'is', 'next', 'Report', 'al', 'the', 'el', 'votaciones', 'financiers', 'cierra', 'votes', 'Nous', 'Ci', 'sance', 'de', 'des', 'interrompue', 'dclare', 'del', 'die', 'der', 'das', 'ist']
SCAN_POLISH_SIGNS=['á', 'à', 'â', 'ä', 'æ', 'ã', 'å', 'ā', 'é', 'è', 'ê', 'ë', 'ė', 'ē', 'ç', 'č', 'ê', 'ô', 'ò', 'õ', 'œ', 'ö', 'ß', 'ü']

def enCheckForWordsAndSigns(tokens):
    return checkForWordsAndSigns(tokens, SCAN_ENGLISH_WORDS, SCAN_ENGLISH_SIGNS)
def plCheckForWordsAndSigns(tokens):
    return checkForWordsAndSigns(tokens, SCAN_POLISH_WORDS, SCAN_POLISH_SIGNS)
def checkForWordsAndSigns(tokens, words, signs):
    for i, token in enumerate(tokens):
        for sign in signs:
            if token.count(sign)>0 and not(isUpper(token[0]) and (i>0 and tokens[i-1] not in ('.', '!', '?'))):
                return False
        if token in words: return False
    return True
