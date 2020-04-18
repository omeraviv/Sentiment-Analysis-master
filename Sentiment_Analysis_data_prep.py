# required libraries

import files_api
from nltk.corpus import stopwords
from os import listdir
import string
import senticnet5
from alphabet_detector import AlphabetDetector

sentiment_dict = senticnet5.senticnet

# ------------------------------------------------------------------- #
#                   DATA PREPROCESSING                                #
# ------------------------------------------------------------------- #


# to clean the file for tokens
def clean_file(file, lang=None):
    tokens = file.split()                                 # split into tokens on whitespace
    table = str.maketrans('', '', string.punctuation)    # remove punctuation
    tokens = [w.translate(table) for w in tokens]

    tokens = [word for word in tokens if word.isalpha()]  # remove non-alphabetic tokens
    set_of_stop_words = set(stopwords.words(lang))   # remove stop words
    if lang == 'arabic':
        with open('lexicon/stop_words_arabic.txt', 'r', encoding='utf-8') as f:
            stop_words_arabic = f.read().split('\n')
            set_of_stop_words = stop_words_arabic + list(set_of_stop_words)
            set_of_stop_words = set(set_of_stop_words)
    tokens = [word for word in tokens if word not in set_of_stop_words]
    return tokens


# to define a vocabulary of words
def add_words_to_vocab_and_update_count(text_list, vocab, lang=None):
        for text in text_list:
            tokens = clean_file(text, lang=lang)   # clean the file
            vocab.update(tokens)        # update count of the word in the vocab


def clean_vocab_min_occurrence(vocab, min_occurrence):
    print('Total Tokens (Before remove min of ', min_occurrence, "occurrences): ", len(vocab))
    tokens = [token for token, count in vocab.items() if count >= min_occurrence]    # list of tokens with count >= 1
    print('Total Tokens (After) : ', len(tokens))
    return tokens



