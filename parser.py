import re
import gc
import sys
import optparse
from xml.dom import minidom
from lxml import etree
#python praser.py -i eutagged000.pl -o eu00

SUBJECT='subject'
VERB='verb'
OBJECT='object'
INTERP='interp'


class XmlConvertor(object):

    def __init__(self, xml_file, infinitive_file, svo_file, combine_file):
        self.xmldoc=etree.iterparse(open(xml_file), events=('end',), tag='chunk')
        self.infinitive_file=open(infinitive_file, 'wb')
        self.svo_file=open(svo_file, 'wb')
        self.combine_file=open(combine_file, 'wb')

        
    def _writeLineToFile(self, line, f, encoding='u8'):
        '''
        write safely data to file if fname is None then print data 
        '''
        f.write(line.encode(encoding)+'\n')
        f.flush()
    
    def _getSVOType(self, ctag):
        '''
        get type of svo by ctag value
        '''
        if "subst" in ctag and "nom" in ctag:
            return SUBJECT
        if "perf" in ctag or "imperf" in ctag:
            return VERB
        if "subst" in ctag:
            return OBJECT
        if "interp" in ctag:
            return INTERP
        import random
        return 'W%d'%random.randint(10, 99)
        return None
      
    def _find_one_replace(self, l):
        '''
        param l: filterd list of tuples
        return: 2 index of words list to replace
        '''
        m={'s': 0, 'v': 1, 'o': 2}
        i=0
        while i+1<len(l):
            if m[l[i][1]]>m[l[i+1][1]]:
                return l[i][0], l[i+1][0]
            i+=1
        return None, None

    def _sortInSvoForm(self, words):
        '''
        param words: [(word, infinitive, svo_type)]
        return: [(word, infinitive, svo_type)] sorted in svo form
        '''
        one_char_type_map=lambda t: 's' if t==SUBJECT else 'v' if t==VERB else 'o' if t==OBJECT else '-'
        one_char_list_map=lambda l: ''.join(map(one_char_type_map, l))
        one_char_tpls_map=lambda l: ''.join([i[1] for i in l])
        reorder_needed=lambda s: set('svo').issubset(set(s.replace('-', '').replace('svo', '')))
        print [i[2] for i in words], one_char_list_map([i[2] for i in words])
        new_words=words[:]
        while True:
            onechars=one_char_list_map([i[2] for i in new_words]) # e.g. '-svovo--ss-'
            # print 'CUR:', onechars
            if not reorder_needed(onechars): break
            tuples=list(enumerate(onechars)) # e.g. [(0, '-'), (1, 's'), (2, 'v'), ...]
            # filter all complete svo
            tuples=[i for i in tuples if i[1]!='-'] # filter '-'
            s=one_char_tpls_map(tuples) # e.g. 'svovoss'
            all_svo_indexes=[i.start() for i in re.finditer('svo', s)]
            for i in all_svo_indexes:
                tuples[i:i+3]=None, None, None
            tuples=[i for i in tuples if i!=None]
            # print 'RDY', one_char_tpls_map(tuples)
            # fine a new replace
            m, n=self._find_one_replace(tuples)
            if m==n==None:
                # print 'BRK'
                break
            new_words[m], new_words[n]=new_words[n], new_words[m]
        print [i[2] for i in new_words], one_char_list_map([i[2] for i in new_words])
        return new_words


    def _prettyFormatSentence(self, words, word_index):
        '''
        return pretty format sentence. e.g: , or . ! must be pasted to previous word
        @param words: list of word structure
        @type words: list
            -> [[(word, infinitive, svo_type)]]
        @param word_index: index of word which must appear in sentenc format.
        @type word_index: int 
        '''
        if len(words)==0:return ''
        sentence=[]
        for i in range(len(words)):
            word, svo_type=words[i][word_index], words[i][-1]
            if i!=0 and svo_type!=INTERP:
                sentence.append(' ')
            sentence.append(word)
        return ''.join(sentence)
    
    def process(self):
        '''
        process xml data and create sentences
        '''
        i=1
        for event, chunk in self.xmldoc:
            if event!='end' or chunk.tag!='chunk':
                continue
            print("chunk #%s"%i)
            sentence=[] # [(word, infinitive, svo_type)]
            for tok in chunk.getchildren():
                children=tok.getchildren()
                if len(children)==0:
                    continue
                word=children[0].text
                children=children[1].getchildren()
                infinitive=children[0].text
                ctag=children[1].text
                svo_type=self._getSVOType(ctag)
                sentence.append((word, infinitive, svo_type))
            #free the memory
            chunk.clear()
            while chunk.getprevious() is not None:
                del chunk.getparent()[0]
            del chunk
            self._writeLineToFile(self._prettyFormatSentence(sentence, 1), self.infinitive_file)
            sortedSvoSentence=self._sortInSvoForm(sentence)
            self._writeLineToFile(self._prettyFormatSentence(sortedSvoSentence, 0), self.svo_file)
            self._writeLineToFile(self._prettyFormatSentence(sortedSvoSentence, 1), self.combine_file)
            i+=1
            #if i%100000==0:
            #    raw_input('1: ')
            #    gc.collect()
            #    raw_input('2: ')

        self.infinitive_file.close()
        self.svo_file.close()
        self.combine_file.close()
        
def parseOptions():
    '''
    parse program parameters
    '''
    usage='usage: %prog [options]'
    parser=optparse.OptionParser(usage=usage)
    parser.add_option('-o', '--out', dest='out', metavar='OUTPUT_FILE', help='path of output pattern, this create separate output for every form with add extension to end of this path')
    parser.add_option('-i', '--in', dest='in_file', metavar='INPUT_FILE', help='path of xml input file')
    options, args=parser.parse_args()
    if not options.in_file:
        parser.error("xml file not given")
    return options, args, parser

def main():
    opt, args, parser=parseOptions()
    infinitive_file=svo_file=combine_file=None
    if opt.out:
        infinitive_file='%s.infinitive'%opt.out
        svo_file='%s.svo'%opt.out
        combine_file='%s.combine'%opt.out
    convertor=XmlConvertor(opt.in_file, infinitive_file, svo_file, combine_file)
    convertor.process()
    #convertor.exportAll(infinitive_file, svo_file, combine_file)
    
if __name__=='__main__':
    main()
    
