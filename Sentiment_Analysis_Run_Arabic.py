import Prep_arabic_dict
import Sentiment_Analysis_data_prep
import Sentiment_Analysis_Bag_of_words
from collections import Counter
import files_api


def run_arabic_senti(all_text_list: list, sentiment=None):

    # prep arab dictionary (words and it's sentiments)
    arab_dict = Prep_arabic_dict.read_csv_to_dict("arabic_lexi.csv", 'utf-8')

    # ------------------------------------------------------------------- #
    #                   DATA PRE-PROCESSING                               #
    # ------------------------------------------------------------------- #

    # to hold tokens and their respective counts. Eg: [('word1',word1_count), ('word2',word2_count),...]
    vocab = Counter()

    # take all words from all docs, clean it, and save it in a 'vocab'
    Sentiment_Analysis_data_prep.add_words_to_vocab_and_update_count(all_text_list,
                                                                     vocab, lang='arabic')

    print('\nThe length of the vocab_arabic before check if we have senti: ', len(vocab))
    print('Top 3 frequently arabic occurring words:', vocab.most_common(3))

    #  removes words that doesn't appear more then min_occ and saves the words as a list.
    min_occurrence = 1
    vocab = Sentiment_Analysis_data_prep.clean_vocab_min_occurrence(vocab, min_occurrence)

    # save vocab to file
    files_api.save_list(vocab, 'vocab_arabic.txt', encoding='utf-8')
    # the vocabulary is saved in a text file for later use

    # ------------------------------------------------------------------- #
    #                   BAG OF WORDS REPRESENTATION                       #
    # ------------------------------------------------------------------- #

    # load the vocabulary
    vocab2 = files_api.load_file("output\\vocab_Arabic.txt", encoding='utf-8')
    vocab2 = vocab2.split()

    # remove words that does not have a senti, and save the new words to file
    print("vocab before: ", len(vocab2), vocab2)
    vocab2, new_words = Sentiment_Analysis_Bag_of_words.check_if_words_have_senti_arabic(vocab2,
                                                                                         arab_dict=arab_dict)
    files_api.save_list(new_words, "new_words_arabic", encoding='utf-8')
    print("vocab after: ", len(vocab2), vocab2)

    # data to lines
    list_of_all_phrases = Sentiment_Analysis_Bag_of_words.reviews_to_lines(
        all_text_list, vocab2, lang='arabic')
    xtrain, index_word = Sentiment_Analysis_Bag_of_words.prepare_data(list_of_all_phrases, mode='freq')
    print("Xtrain shape: ", xtrain.shape)
    results_list = []
    for i in range(len(list_of_all_phrases)):
        results = {'Original Text': list_of_all_phrases[i][0],
                   'Original Tag': sentiment,
                   # 'Senti Words': list_of_all_phrases[i][1],
                   'Senti Score': Sentiment_Analysis_Bag_of_words.calc_senti_of_line_arabic(xtrain[i], index_word, arab_dict)}
        results_list.append(results)

    return results_list