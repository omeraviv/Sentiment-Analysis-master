# required libraries

from nltk.corpus import stopwords
from collections import Counter
from os import listdir
import numpy as np
import string
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense
from keras import utils
import csv
from os.path import join

# -------------------------------------------------------------------#
#                   DATA PREPROCESSING                              #
# -------------------------------------------------------------------#


def load_file(filepath, lang=None):
    if(lang):
        encoding=None
    else:
        encoding='utf-8'
    try:
        file = open(filepath, 'r', encoding=encoding)  # open the file in the read only mode
        text = file.read()  # read the contents of the file
        file.close()  # close the file
    except:
        file = open(filepath, 'r', encoding='utf-8')  # open the file in the read only mode
        text = file.read()  # read the contents of the file
        file.close()  # close the file
    return text


def load_file_vocab(filepath):
    file = open(filepath, 'r', encoding='utf-8')  # open the file in the read only mode
    text = file.read()  # read the contents of the file
    file.close()  # close the file
    return text


# to clean the file for tokens
def clean_file(file, lang='english'):
    tokens = file.split()  # split into tokens on whitespace

    table = str.maketrans('', '', string.punctuation)  # remove punctuation
    tokens = [w.translate(table) for w in tokens]

    tokens = [word for word in tokens if word.isalpha()]  # remove non-alphabetic tokens

    set_of_stop_words = set(stopwords.words(lang))  # remove stop words
    tokens = [word for word in tokens if not word in set_of_stop_words]

    tokens = [word for word in tokens if len(word) > 1]  # remove tokens of length <= 1

    return tokens


# to define a vocabulary of words
def add_words_to_vocab_and_update_count(text_list, vocab, lang=None):
    for text in text_list:
        if(lang):
            tokens = clean_file(text, lang=lang)
        else:
            tokens = clean_file(text, lang='arabic') # load the file
          # clean the file
        vocab.update(tokens)  # update count of the word in the vocab


def save_list(lines, filename):
    data = '\n'.join(lines)
    file = open(filename, 'w', encoding='utf-8')
    file.write(data)
    file.close()


def reviews_to_lines(text_list, vocab, lang=None, senti=None):
    lines = []
    original_text = []
    labels = []
    for review_text in text_list:
        if lang:
            original_text.append(review_text)
            labels.append(senti)
            tokens = clean_file(review_text, lang=lang)  # clean the file
        else:
            original_text.append(review_text)
            labels.append(senti)
            tokens = clean_file(review_text, lang='arabic')  # clean the file

        tokens = [word for word in tokens if word in vocab]  # filter by vocab

        line = ' '.join(tokens)  # single review -> tokens -> filter -> single line with tokens spaced by whitespace
        lines.append(line)  # list of reviews. Single review is stored at each index of the list
    return lines, original_text, labels


def prepare_data(train_reviews, test_reviews, mode):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(train_reviews)  # fit the tokenizer on the texts
    xtrain = tokenizer.texts_to_matrix(train_reviews, mode=mode)  # encode the training set
    xtest = tokenizer.texts_to_matrix(test_reviews, mode=mode)  # encode the test set

    return xtrain, xtest


def save_results(path, filename, text, labels_test, prediction):
    with open(join(path, filename), 'w', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Text', "Label", 'Predicted Senti', 'Predicted Score'))
        for i in range(len(text)):
            if prediction[i][0] >= 0.5:
                predicted_senti = "Negative"
            else:
                predicted_senti = "Positive"
            writer.writerow([text[i], labels_test[i], predicted_senti, prediction[i][0]])


# the training/learning model
def seniment_analysis_model(xtrain, ytrain, epochs=10):
    n_words = xtrain.shape[1]
    # define the network
    model = Sequential()
    model.add(Dense(50, input_shape=(n_words,), activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # compile the network
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit the network to the training data
    history = model.fit(xtrain, ytrain, epochs=epochs
                        , verbose=2)
    return model, history


def sentiment_analysis_model_run(train_pos_reviews, train_neg_reviews, test_pos_reviews, test_neg_reviews, file_to_save : str, lang=None, epochs=10):

    train_pos_len = len(train_pos_reviews)
    test_pos_len = len(test_pos_reviews)

    vocab = Counter()  # to hold tokens and their respective counts. Eg: [('tok1',tok1_count), ('tok2',tok2_count),...]

    add_words_to_vocab_and_update_count(train_pos_reviews, vocab, lang=lang)
    add_words_to_vocab_and_update_count(train_neg_reviews, vocab, lang=lang)
    print('The length of the vocab: ', len(vocab))
    print('\nTop 10 frequently occuring words:', vocab.most_common(10))

    min_occurrence = 2

    print('Total Tokens (Before): ', len(vocab))
    tokens = [token for token, count in vocab.items() if count >= min_occurrence]  # list of tokens with count >= 2
    print('Total Tokens (After) : ', len(tokens))

    save_list(tokens, 'vocab.txt')  # the vocabulary is saved in a text file for later use


    # -------------------------------------------------------------------#
    #                   BAG OF WORDS REPRESENTATION                     #
    # -------------------------------------------------------------------#

    # load the vocabulary
    vocab = load_file("vocab.txt", lang=lang)
    vocab = vocab.split()
    vocab = set(vocab)

    # Training Data : reviews to lines
    train_pos_reviews_to_lines, original_text_train_pos, labels_train_pos = reviews_to_lines(train_pos_reviews, vocab, lang=lang, senti="Positive")
    train_neg_reviews_to_lines, original_text_train_neg, labels_train_neg = reviews_to_lines(train_neg_reviews, vocab, lang=lang, senti="Negative")

    # Test Data : reviews to lines
    test_pos_reviews_to_lines, original_text_pos, labels_test_pos = reviews_to_lines(test_pos_reviews, vocab, lang=lang, senti="Positive")
    test_neg_reviews_to_lines, original_text_neg, labels_test_neg = reviews_to_lines(test_neg_reviews, vocab, lang=lang, senti="Negative")

    # Total training and testing data
    train_reviews = train_pos_reviews_to_lines + train_neg_reviews_to_lines
    test_reviews = test_pos_reviews_to_lines + test_neg_reviews_to_lines
    original_text_test = original_text_pos + original_text_neg
    labels_test = labels_test_pos + labels_test_neg

    xtrain, xtest = prepare_data(train_reviews, test_reviews, mode='freq')

    print(" Shape of xtrain: ", xtrain.shape)
    print(" Shape of xtest : ", xtest.shape)

    #train_pos_limit = int(xtrain.shape[0] / 2)  # upper limit of pos training reviews
    #train_neg_limit = xtrain.shape[0]  # upper limit of neg training reviews
    #test_pos_limit = int(xtest.shape[0] / 2)  # upper limit of pos test reviews
    #test_neg_limit = xtest.shape[0]  # upper limit of neg test reviews

    ytrain = np.array([0 for i in range(train_pos_len)] + [1 for i in range(train_pos_len, xtrain.shape[0])])
    ytest = np.array([0 for i in range(test_pos_len)] + [1 for i in range(test_pos_len, xtest.shape[0])])

    # -------------------------------------------------------------------#
    #                   SENTIMENT ANALYSIS MODEL                        #
    # -------------------------------------------------------------------#

    classifier, model_history = seniment_analysis_model(xtrain, ytrain, epochs=epochs)
    # evaluation of the preformance of the trained model on the test set
    loss, accuracy = classifier.evaluate(xtest, ytest, verbose=0)
    prediction = classifier.predict(xtest)
    print('Test accuracy = ', (accuracy * 100))

    save_results('output/', file_to_save, original_text_test, labels_test, prediction)


# sentiment_analysis_model_run(file_to_save="arabic_results_learning.csv", train_set_pos_path=train_set_pos_path, train_set_neg_path=train_set_neg_path, test_set_pos_path=test_set_pos_path, test_set_neg_path=test_set_neg_path)