# -*- coding: utf-8 -*-

"""
    In this file, there are three kinds of tokenizer tools, used to tokenize 
tweets, respectively from nltk module, cmu twitter mining team(ark tokenizer) and
stanford nlp team(stanford tokenizer).
    In order to work out short unstructed text mining, such as tweets and status,
the tokenizer must be able to 'requisitely' tokenize the short text and
'additionally' pick out special social text phrase, such as user mentions, urls
and hashtags.
    1.nltk
        CANs    : basically tokenizinge text, just like splitting by white spaces
        CANNOTs : picking out special phrases(eg. urls).
    2.cmu
        CANs    : tokenizing short texts
                  picking out hashtags
                  picking out urls
                  picking out user mentions
                  picking out emoticon ( :) )
        CANNOTs : picking out file names
    3.stanford
        CANs    : tokenizing short texts
                  picking out hashtags
                  picking out user mentions
                  picking out file names.
        CANNOTs : it even cannot split the full stop from the last word, for the
                  reason this tokenizer cannot execute '.' that it could pick
                  out file names. IT CANNOT EXECUTE FULL STOP :)
    So, we will suspend nltk tokenizer in this case, choosing ark tokenizer (for
little influence caused by file names) or stanford tokenizer to tokenize the
texts after filtered urls.
"""

import json
from nltk.tokenize      import word_tokenize
from nltk.tokenize      import wordpunct_tokenize
from tokenizer_ark      import tokenizeRawTweetText
from tokenizer_stanford import Tokenizer as STokenizer
from nltk.stem.wordnet  import WordNetLemmatizer as Lemmatizer

def tokenize_ark(text):

    return tokenizeRawTweetText(text)

def tokenize_nltk(text):

    return word_tokenize(text)

def tokenize_stf(text):

    tok = STokenizer(preserve_case=False)
    return tok.tokenize(text)

# [tokenizer_bat]
# @input: peer_id
# @brief: tokenize all tweets of a peer
#         1. store in the mongodb directly
#         2. modify the tokenization flag bit
def tokenizer_bat(coll, username):

    peer    = coll.find_one({'username': username})
    texts   = peer['texts']
    count_s = 0
    count_w = 0

    lemmatizer = Lemmatizer()

    for text in texts:

        flag   = text['flag']
        content= text['content']

        # memo: the first flag bit refer to tokenization flag bit.
        if flag[0:1] == '0':

            # tokenization
            tokens = tokenize_ark(content)

            # normalization
            for i in range(len(tokens)):
                tokens[i]  = lemmatizer.lemmatize(tokens[i])

            # lower
            lowers = []
            for i in range(len(tokens)):
                lowers.append(tokens[i].lower())

            text['tokens']      = tokens
            text['token_lower'] = lowers

            text['flag'] = '1' + flag[1:]
            count_s     +=  1

        elif flag[0:1] == '1':

            count_w     +=  1

        else:

            pass

    coll.update_one({'username':username}, {'$set':{'texts':texts}})
    print "SUCC: Tokenization done." 
    print "STAT: %s texts executed and %s texts have been executed before." \
            % (count_s, count_w)


def print_token(tokens):

    for token in tokens:
        print token,

if __name__ == "__main__":

    sample = [
        'DENNIS: Listen, strange women lying in ponds distributing swords is no basis for a system of government.  Supreme executive power derives from a mandate from the masses, not from some farcical aquatic ceremony.',
        'Some programmers, when confronted with a problem, think "I know, I\'ll use floating point arithmetic." Now they have 1.999999999997 problems.', 
        'Photoshop?! #Wow pic.twitter.com/Z0mseCRi',
        'Python\'s sys.float_info is analogous to C\'s float.h header.',
        'RT @SciPyTip:Research Tools ow.ly/8WMpb Videos and notes on Python, Emacs, bash, etc.',
        'About unicode (and Python) nedbatchelder.com/text/unipain.h',
        '^_^ Learning from @b_entwistle &@pr_chambers about #Snippets in #Sublime - cool stuff! computationalmodelling.bitbucket.org/tools/sublime. #NGCM #CDT pic.twitter.com/DS135EKI9H :)'
    ]

    for text in sample:
        print "-" * 50
        print "text     :", text
        print "nltk     :", print_token(tokenize_nltk(text))
        print "ark      :", print_token(tokenize_ark(text))
        print "stanford :", print_token(tokenize_stf(text))
