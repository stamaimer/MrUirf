import json

from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize

from ark_tokenizer      import tokenizeRawTweetText
from stanford_tokenizer import Tokenizer as STokenizer

def tokenize_ark(text):
    return tokenizeRawTweetText(text)

def tokenize_nltk(text):
    return word_tokenize(text)

def tokenize_stf(text):
    tok = STokenizer(preserve_case=False)
    return tok.tokenize(text)

def print_token(tokens):
    for token in tokens:
        print token,

if __name__ == "__main__":

    sample = [
        'Some programmers, when confronted with a problem, think "I know, I\'ll use floating point arithmetic." Now they have 1.999999999997 problems.', 
        'Photoshop?! #Wow pic.twitter.com/Z0mseCRi',
        'Python\'s sys.float_info is analogous to C\'s float.h header.',
        'RT @SciPyTip:Research Tools ow.ly/8WMpb Videos and notes on Python, Emacs, bash, etc.',
        'About unicode (and Python) nedbatchelder.com/text/unipain.h']

    for text in sample:
        print "-" * 50
        print "texr     :", text
        print "nltk     :", print_token(tokenize_nltk(text))
        print "ark      :", print_token(tokenize_ark(text))
        print "stanford :", print_token(tokenize_stf(text))
