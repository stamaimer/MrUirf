# -*- coding: utf-8 -*-

'''
    In this file we include several normalization tools from nltk. The purpose
of these is stemming or lemmatizing words.
    First of all, paying attention to the func'normalize_match_sample', in the
defination block we have a corpus 'kwlist' and a normalization function
'get_close_matches'. We use normalization function to corrent fuzzy word 'fuzzyw'
by mapping it from a authentic corpus. These tools are integrated funcs with a 
corpus and normalization funtion inside.
    Finally we determined to use nltk wordnet lemmatizer, and lemmatizing is
enough comparing to stemming.
'''

import json
import difflib
from nltk.tokenize          import word_tokenize
from nltk.stem.lancaster    import LancasterStemmer
from nltk.stem.porter       import PorterStemmer
from nltk.stem.snowball     import SnowballStemmer
from nltk.stem.wordnet      import WordNetLemmatizer

def normalize_match_sample():
    fuzzyw = 'ape'
    kwlist = ['apple', 'peach', 'pear']
    print difflib.get_close_matches(fuzzyw, kwlist)

def normalize_nltk_lancaster(token):
    lancaster = LancasterStemmer()
    return lancaster.stem(token)

def normalize_nltk_porter(token):
    porter = PorterStemmer()
    return porter.stem(token)

def normalize_nltk_snowball(token):
    # choose language english firstly
    # or you could import snowball englishstemmer directly
    #   use 'print(" ".join(SnowballStemmer.languages))))' to 
    #   check what languages snowball supports
    snowball = SnowballStemmer('english')
    return snowball.stem(token)

def normalize_nltk_lemmatizer(token):
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(token)

if __name__ == "__main__":

    sample = [
        u'Blog entry: summary of Weiwei Wang’s new PRL on magnon driven domain wall motion with DMI',
        u'@IanBDunne Our kids are still excited about Barbie being pushed of the Van-der-Graaf generator from the pressure wave. Good job!',
        u'#piday2015 works best in American date notation. Still nice, though.',
        u'these women taught English, they are now lying here!'
    ]

    for text in sample:
        tokens = word_tokenize(text)
        matrix = [['raw', 'lancaster', 'porter', 'snowball', 'lemmatizer']]
        for token in tokens:
            row = [token]
            row.append(normalize_nltk_lancaster(token))
            row.append(normalize_nltk_porter(token))
            row.append(normalize_nltk_snowball(token))
            row.append(normalize_nltk_lemmatizer(token))
            matrix.append(row)

        print '-'*50
        print text.encode('utf8')
        for row in matrix:
            for token in row:
                if len(token) >= 8: print token.encode('utf8')+'\t',
                else:               print token.encode('utf8')+'\t\t',
            print
