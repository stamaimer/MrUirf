import json

from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize

def tokenize_nltk(sentence):
    return word_tokenize(sentence)

if __name__ == "__main__":

    with open('tweets.json', 'r') as f:
        source = f.read()
    tweets = json.JSONDecoder().decode(source)

    for item in tweets[0]['Hans Fangoh']:
        item['tokens'] = tokenize_nltk(item['tweet'])
        print item['tokens']
