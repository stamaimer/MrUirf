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

# [pos_bat]
# @input: peer_id
# @brief: pos tag all texts of a peer
#         1. store in mongodb directly
#         2. modify pos tagging flag bit
def pos_bat(coll, peer_id):

    peer    = coll.find_one({'_id': peer_id})
    texts   = peer['texts']
    count_s = 0
    count_w = 0

    for text in texts:

        flag   = text['flag']
        content= text['content']

        # memo: 
        #   the first flag bit refer to tokenization flag bit.
        #   the second flag bit refer to pos tagging flag bit.
        if flag[0:1] == '1' and flag[1:2] == '0':

            tokens  = text['tokens']

            # pos tagging
            tokens_p= pos_tag(tokens)

            text['pos'] = tokens_p

            text['flag']= flag[0:1] + '1' + flag[2:]
            count_s += 1

        else:

            count_w += 1

    coll.update_one({'_id':peer_id}, {"$set": {'texts': texts}})
    print "SUCC: POS tagging done."
    print "STAT: %s texts executed and %s texts have been executed before." \
            % (count_s, count_w)

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
