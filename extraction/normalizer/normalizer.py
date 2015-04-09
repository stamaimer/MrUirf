import json
import difflib
from nltk.stem.lancaster    import LancasterStemmer
from nltk.stem.porter       import PorterStemmer
from nltk.stem.snowball     import SnowballStemmer
from nltk.stem.wordnet      import WordNetLemmatizer
from ..tokenizer.ark_tokenizer import tokenizeRawTweetText

def tokenize(text):
    return tokenizeRawTweetText(text)

def normalize_match(token):
    kwlist = ['apple', 'peach', 'pear']
    return difflib.get_close_matches(token, kwlist)

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

    print normalize_match('app')

    source = file('../tweets.json')
    target = json.load(source)
    tweets = target[0]['Hans Fangoh']
    print tweets
