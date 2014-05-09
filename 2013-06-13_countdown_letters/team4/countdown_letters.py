import string
import random

# file containing the words file to use to generate possible words
WORDSFILE = "/usr/share/dict/words"

def get_choices():
    """Function to ask user for choices"""
    cv=[]
    for i in range(9):
        while True:
            choice=raw_input("choose consonant(c) or vowel(v)")
            if choice=="c" or choice == "v":
                cv.append(choice)
                break
            else:
                print "please choose again"

    return cv

def get_letters(choices):
    """Returns list of consonant or vowel"""
    all_letters = set(string.ascii_uppercase)
    vowels = set("aeiou")
    consonants = all_letters - vowels
    letters = []

    for choice in choices:
        if choice == "v":
            letters.append(random.choice(list(vowels)))
        else:
            letters.append(random.choice(list(consonants)))
    return letters

def all_subsets(ls):
    """Returns all the combinations of the list ls. IE all subsets of the list.
    
    NB could use itertools.combinations(ls, n) and looping over all the values
    of n from 1 to len(ls) + 1. """
        
    ret = []
    for n in range(1, len(ls)+1):
        ret.extend(subset(ls,n))
    return ret 
        
def subset(ls, n):
    """Returns the subsets of the list of size n, this is the same as the
    choosing sets of size n from the all the combinations of size n  possible from the
    list."""
    if n == 0:
        return [[]]
    if ls == []:
        return []
    return [ls[:1] + s for s in subset(ls[1:], n-1)] + subset(ls[1:], n)
    

def get_all_words(letters):
    poss_words = []
    flines = open(WORDSFILE).readlines()
    dict_words = [line.strip().upper() for line in flines]
    # need all combinations of letters

    combinations = [sorted(comb) for comb in all_subsets(letters)]

    for word in dict_words:
        s_word = sorted(word)
        # are all the characters in s_word in letters?
        if s_word in combinations:
            poss_words.append((len(word), word))
    
    return sorted(poss_words, reverse=True)

if __name__ == "__main__":
    cvs=get_choices()
    letters= get_letters(cvs)
    #letters = list("ADVENTURE")
    print "Your letters are:"
    print letters

    print "Possible words are:"
    for w in get_all_words(letters):
        print w[0], w[1]
