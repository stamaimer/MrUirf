import difflib

def normalize_match(token):
    kwlist = ['apple', 'peach', 'pear']
    return difflib.get_close_matches(token, kwlist)


if __name__ == "__main__":

    print normalize_match('app')
