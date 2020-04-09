import Sentiment_Analysis_data_prep
import Sentiment_Analysis_Bag_of_words
from collections import Counter
import files_api


"""
returns list of dicts with the results in the following format:
    file_names[i]: xxx
    'senti_words': xxx
    'senti_score': xxx
 """
def run_eng_senti(text_list: list, sentiment=None):

    # ------------------------------------------------------------------- #
    #                   DATA PRE-PROCESSING                                #
    # ------------------------------------------------------------------- #

    # to hold tokens and their respective counts. Eg: [('word1',word1_count), ('word2',word2_count),...]
    vocab = Counter()

    # take all words from all docs, clean it, and save it in a 'vocab'
    Sentiment_Analysis_data_prep.add_words_to_vocab_and_update_count(text_list,
                                                                     vocab)

    print('The length of the vocab before check if we have senti: ', len(vocab))
    print('Top 3 frequently occuring words:', vocab.most_common(3))

    #  removes words that doesn't appear more then min_occ and saves the words as a list.
    min_occurrence = 1
    vocab = Sentiment_Analysis_data_prep.clean_vocab_min_occurrence(vocab, min_occurrence)

    # save vocab to file
    files_api.save_list(vocab, 'vocab.txt')   # the vocabulary is saved in a text file for later use

    # ------------------------------------------------------------------- #
    #                   BAG OF WORDS REPRESENTATION                       #
    # ------------------------------------------------------------------- #

    # load the vocabulary
    vocab2 = files_api.load_file("output\\vocab.txt")
    vocab2 = vocab2.split()

    # remove words that does not have a senti, and save the new words to file
    print("vocab before: ", len(vocab2))
    vocab2, new_words = Sentiment_Analysis_Bag_of_words.check_if_words_have_senti(vocab2)
    files_api.copy_to_json(new_words, "new_words_eng")
    print("vocab after: ", len(vocab2))
    # Training Data : reviews to lines
    list_of_all_phrases = Sentiment_Analysis_Bag_of_words.reviews_to_lines(text_list, vocab2)

    xtrain, index_word = Sentiment_Analysis_Bag_of_words.prepare_data(list_of_all_phrases, mode='freq')
    print("Xtrain shape: ", xtrain.shape)

    results_list = []
    for i in range(len(list_of_all_phrases)):
        results = {'Original text': list_of_all_phrases[i][0],
                   'Senti words': list_of_all_phrases[i][1],
                   'Original Tag': sentiment,
                   'Senti score': Sentiment_Analysis_Bag_of_words.calc_senti_of_line(xtrain[i], index_word)}
        results_list.append(results)

    return results_list


