# -*- coding: utf-8 -*-

from nltk.tokenize      import word_tokenize
from nltk               import pos_tag
from nltk.tag.stanford  import POSTagger
from nltk.tag.stanford  import NERTagger

def pos_nltk(tokens):

    return pos_tag(tokens)

def pos_stanford(tokens):

    tagger = POSTagger('./english-bidirectional-distsim.tagger',
                       './stanford-postagger.jar')
    return tagger.tag(tokens)

if __name__ == "__main__":

    sample = [
        'these women taught English, they are now lying here!',
    ]

    for text in sample:
        tokens = word_tokenize(text)
        matrix = [['raw', 'nltk', 'stanford']]
        nltk_p = pos_nltk(tokens)
        stan_p = pos_stanford(tokens)[0]
        for i in range(len(tokens)):
            row = [tokens[i]]
            row.append(nltk_p[i][1])
            row.append(stan_p[i][1])
            matrix.append(row)

        print '-'*50
        print text.encode('utf8')
        for row in matrix:
            for token in row:
                if len(token) >= 8: print token.encode('utf8')+'\t',
                else:               print token.encode('utf8')+'\t\t',
            print

    # snerer = NERTagger('english.all.3class.distsim.crf.ser.gz',
    #                    'stanford-ner.jar')
    # print snerer.tag(sample[0])
