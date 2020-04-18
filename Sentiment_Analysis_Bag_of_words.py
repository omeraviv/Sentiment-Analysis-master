from os import listdir
import senticnet5
from keras.preprocessing.text import Tokenizer
from Sentiment_Analysis_data_prep import clean_file
import files_api
import os.path

# sentiment_dict = senticnet5.senticnet

def create_dict_of_sentiments(data_path):
    lexi = {}
    with open(os.path.join(data_path, 'positive-words.txt'), 'r') as pf:
        pos_words = pf.read().split('\n')
    with open(os.path.join(data_path, 'negative-words.txt'), 'r') as nf:
        neg_words = nf.read().split('\n')
    for word in pos_words:
        lexi[word] = 1
    for word in neg_words:
        lexi[word] = -1
    return lexi

sentiment_dict = create_dict_of_sentiments('lexicon/')

# ------------------------------------------------------------------- #
#                   BAG OF WORDS REPRESENTATION                       #
# ------------------------------------------------------------------- #


# ignore words that dont have sentiment in the dict
def check_if_words_have_senti(vocab,  lang=None, arab_dict=None):
        words_from_vocab_with_senti = [word for word in vocab if word in sentiment_dict.keys()]
        new_words = [word for word in vocab if word not in words_from_vocab_with_senti]
        return words_from_vocab_with_senti, new_words


def check_if_words_have_senti_arabic(vocab, arab_dict):
        words_from_vocab_with_senti = [word for word in vocab if word in arab_dict.keys()]
        new_words = [word for word in vocab if word not in words_from_vocab_with_senti]
        return words_from_vocab_with_senti, new_words


def get_senti_of_word(word, dict_of_sentiments: dict):
    return dict_of_sentiments[word]
    #return dict_of_sentiments[word][7]


def get_senti_of_word_arabic(word, dict_of_sentiments: dict):
    return dict_of_sentiments[word]


def add_sentiment_to_vocab(vocab, dict_of_sentiments: dict) -> dict:
    vocab_with_senti = {}
    for word in vocab:
        vocab_with_senti[word] = get_senti_of_word(word, dict_of_sentiments)
    return vocab_with_senti


# to generate list of reviews
def reviews_to_lines(text_list : list, vocab,  lang=None):
    text_elements = []
    for text in text_list:
        text_and_tokens = []
        original_text = text
        tokens = clean_file(text, lang=lang)   # clean the file
        tokens = [word for word in tokens if word in vocab]   # filter by vocab
        if len(tokens) < 1:
            continue
        line = ' '.join(tokens)     # single review -> tokens -> filter -> single line with tokens spaced by whitespace
        text_and_tokens.append(original_text)
        text_and_tokens.append(line)
        # list of reviews. Single review is stored at each index of the list
        text_elements.append(text_and_tokens)
    return text_elements


# to prepare the data for training using Bag-Of-Words model
def prepare_data(train_reviews, mode):
    tokenizer = Tokenizer()
    clean_texts_list = [y for [x,y] in train_reviews]
    tokenizer.fit_on_texts(clean_texts_list) # fit the tokenizer on the texts
    matrix_text = tokenizer.texts_to_matrix(clean_texts_list, mode = mode)  # encode the training set
    index_word = tokenizer.index_word
    return matrix_text, index_word


def calc_senti_of_line(line, dict_of_words):
    negative_freq = 0
    for i in range(1, len(line)):
        freq = line[i]
        if freq != 0:
            senti = float(get_senti_of_word(dict_of_words[i], sentiment_dict))
            if senti < 0:
                negative_freq += freq
    #total = float(negative_count) / len_count
    return 'Positive, {}'.format(negative_freq) if negative_freq < 0.21 else 'Negative, {}'.format(negative_freq)


def calc_senti_of_line_arabic(line, index_word, arab_dict):
    negative_freq = 0
    for i in range(1, len(line)):
        freq = line[i]
        if freq != 0:
            senti = float(get_senti_of_word_arabic(index_word[i], arab_dict))
            if senti == -0.2:
                negative_freq += freq * 0.5
            elif senti == -1:
                negative_freq += freq
    return 'Positive' if negative_freq < 0.32 else 'Negative'
