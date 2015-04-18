# -*- coding: utf-8 -*-

from nltk.tokenize      import word_tokenize
from nltk               import pos_tag
from nltk.tag.stanford  import POSTagger

def pos_nltk(tokens):

    return pos_tag(tokens)

def pos_stanford(tokens):

    tagger = POSTagger('./english-bidirectional-distsim.tagger',
                       './stanford-postagger.jar')
    return tagger.tag(tokens)

def pos_bat(coll, peer_id):
    pass

if __name__ == "__main__":

    sample = [
        u'Blog entry: summary of Weiwei Wang’s new PRL on magnon driven domain wall motion with DMI',
        u'@IanBDunne Our kids are still excited about Barbie being pushed of the Van-der-Graaf generator from the pressure wave. Good job!',
        u'#piday2015 works best in American date notation. Still nice, though.',
        u'these women taught English, they are now lying here!'
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
