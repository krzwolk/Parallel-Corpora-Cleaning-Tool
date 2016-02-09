# encoding: utf8

from config import *
import nltk
import json
import pprint
import re
import os
from rules import *

class ManualCorrectionLogger(object):
    def __init__(self, fname):
        self.l=[]
        self.fname=fname
    def log(self, i, line, language):
        print('%s, %s\n%s*******************'%(i, language, line))
        self.l.append({'i': i, 'line': line, 'language': language})
    def commit(self):
        f=open(self.fname, 'w')
        for d in self.l: f.write(json.dumps(d)+'\n')
        f.close()

def clean():
    global EN, PL
    if EN: finEn=open(INPUT_EN)
    if PL: finPl=open(INPUT_PL)
    if EN: fInterEn=open(INTER_EN, 'wb')
    if PL: fInterPl=open(INTER_PL, 'wb')
    lineIndex=0
    mnlogger=ManualCorrectionLogger(MANUAL_CLEAN_FILENAME)
    while True:
        if EN: lineEn=finEn.readline().strip()
        if PL: linePl=finPl.readline().strip()
        if EN and lineEn=='': break
        if PL and linePl=='': break
        if EN: lineEn=unicode(lineEn, 'utf-8', 'ignore').encode('utf-8')
        if PL: linePl=unicode(linePl, 'utf-8', 'ignore').encode('utf-8')
        if EN and hasLinkOrXML(lineEn):
            print('deleted line %s:\n%s*********************'%(lineIndex, lineEn))
            continue
        if PL and hasLinkOrXML(linePl):
            print('deleted line %s:\n%s*********************'%(lineIndex, linePl))
            continue
        
        lineIndex+=1
        if EN: tokensEn=nltk.word_tokenize(lineEn)
        if PL: tokensPl=nltk.word_tokenize(linePl)
        if EN and not enCheckForWordsAndSigns(tokensEn): mnlogger.log(lineIndex, lineEn, 'en')
        if PL and not plCheckForWordsAndSigns(tokensPl): mnlogger.log(lineIndex, linePl, 'pl')
        if EN: lineEn=capitalizedLower(lineEn)
        if PL: linePl=capitalizedLower(linePl)
        if EN: lineEn=enSymbolCharReplace(lineEn)
        if PL: linePl=plSymbolCharReplace(linePl)
        if EN: lineEn=removeTraillingWhiteSpaces(lineEn)
        if PL: linePl=removeTraillingWhiteSpaces(linePl)
        if EN: lineEn=removeIgnoreChars(lineEn)
        if PL: linePl=removeIgnoreChars(linePl)
        if EN: lineEn=capitalizedLower(lineEn)
        if PL: linePl=capitalizedLower(linePl)
        if EN: fInterEn.write(lineEn.strip()+'.\n')
        if PL: fInterPl.write(linePl.strip()+'.\n')
    mnlogger.commit()
    if EN: finEn.close()
    if PL: finPl.close()
    if EN: fInterEn.close()
    if PL: fInterPl.close()

def manualCorrection():
    global EN, PL
    f=open(MANUAL_CLEAN_FILENAME)
    replacement={}
    while True:
        s=f.readline()
        if len(s)==0: break
        if len(s.strip())==0: continue
        d=json.loads(s)
        if (not EN) and d['language']=='en': continue
        if (not PL) and d['language']=='pl': continue
        s=raw_input('Current Line: %sEnter your line (Press enter to skip just this line, or Enter skip to skip all): '%d['line'].encode('u8'))
        if s.strip()=='skip': break
        if s.strip()!='': replacement['%s_%s'%(d['language'],d['i'])]=s+'\n'
    f.close()
    if EN: fInterEn=open(INTER_EN)
    if PL: fInterPl=open(INTER_PL)
    if EN: foutEn=open(OUTPUT_EN, 'w')
    if PL: foutPl=open(OUTPUT_PL, 'w')
    lineIndex=0
    while True:
        lineIndex+=1
        if EN: lineEn=fInterEn.readline()
        if PL: linePl=fInterPl.readline()
        if EN and lineEn=='': break
        if PL and linePl=='': break
        if EN and 'en_%s'%lineIndex in replacement: foutEn.write(replacement['en_%s'%lineIndex])
        elif EN: foutEn.write(lineEn)
        if PL and 'pl_%s'%lineIndex in replacement: foutPl.write(replacement['pl_%s'%lineIndex])
        elif PL: foutPl.write(linePl)
    if EN: fInterEn.close()
    if PL: fInterPl.close()
    if EN: foutEn.close()
    if PL: foutPl.close()

def checkSpell():
    if EN: os.system('aspell -l en -c input.en.txt --ignore-case')
    if PL: os.system('aspell -l pl -c input.pl.txt --ignore-case')
def main():
    global EN, PL
    EN=PL=False
    import cProfile
    qspell=raw_input('Do you want to run spell checking? (yes/no) ')
    qclean=raw_input('Do you want to clean? (yes/no) ')
    qcorrection=raw_input('Do you want to run manual correction? (yes/no) ')
    
    c2=raw_input('1. just English, 2. just Polish, 3. English and Polish\nEnter choice: ')
    if c2 in ('1', '3'): EN=True
    if c2 in ('2', '3'): PL=True
    if qspell.lower()=='yes': checkSpell()
    if qclean.lower()=='yes': clean()
    if qcorrection.lower()=='yes': manualCorrection()
    
if __name__=='__main__':
    main()