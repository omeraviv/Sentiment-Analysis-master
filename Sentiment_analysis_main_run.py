import googletrans
from Sentiment_Analysis_Run_Eng import run_eng_senti
from Sentiment_Analysis_Run_Arabic import run_arabic_senti
from Sentiment_Analysis_Learning_Model import sentiment_analysis_model_run
import load_tweets
import files_api
import os.path
import json
import Sentiment_Analysis_Translate
from os import listdir


# english_data_path = "Data/myData/ENG/"
# training and test data paths


# load_tweets.save_tweets_to_text_files2('Data/Tweets/')
# Sentiment_Analysis_Translate.translate_all_tweets()
def text_files_to_list(data_dir_pos, data_dir_neg, encoding=None):
    pos_text_list = []
    neg_text_list = []
    for filename in listdir(data_dir_pos):
        file_path = os.path.join(data_dir_pos, filename)
        try:
            text = files_api.load_file(file_path, encoding=encoding)  # load the file
        except ValueError:
            print('error load file name: {}, to the texts list'.format(filename))
            continue
        pos_text_list.append(text)
    for filename in listdir(data_dir_neg):
        file_path = os.path.join(data_dir_neg, filename)
        try:
            text = files_api.load_file(file_path, encoding=encoding)  # load the file
        except ValueError:
            print('error load file name: {}, to the texts list'.format(filename))
            continue
        neg_text_list.append(text)
    return pos_text_list, neg_text_list


def text_single_file_to_list(data_dir, filename, encoding=None):
    with open(os.path.join(data_dir, filename), 'r', encoding=encoding) as out_file:
        text = out_file.readlines()
        return text


def list_to_files(text_list, save_path, file_name, encoding=None):
    counter = 0
    for text in text_list:
        with open(os.path.join(save_path, file_name + str(counter)), 'w', encoding=encoding) as out_file:
            out_file.write(text)
        counter += 1

def json_reviews_to_list(data_path):
    with open(data_path, 'r') as file:
        json_data_list = [json.loads(line) for line in file]
        positive_list = []
        negative_list = []
        counter = 0
        for data in json_data_list:
            over_all = data["overall"]
            if over_all < 3:
                negative_list.append(data["reviewText"].lower())
                counter += 1
        for data in json_data_list:
            over_all = data["overall"]
            if over_all > 3 and counter > 0:
                positive_list.append(data["reviewText"].lower())
                counter -= 1
        return positive_list, negative_list


def seperate_to_train_and_test(data_list : list, test_factor : float):
    test_list = []
    length = len(data_list)
    for index in range(int(length * test_factor)):
        test_list.append(data_list.pop())
    return data_list, test_list


def list_to_pos_neg_arabic(data : list):
    pos_list = []
    neg_list = []
    counter_P = 0
    counter_N = 0
    for text in data:
        senti_text = text.split('\t')
        if senti_text[0] == "Positive" and counter_P<=7499:
            pos_list.append(senti_text[1])
            counter_P += 1
        elif senti_text[0] == "Negative" and counter_N<=7499:
            neg_list.append(senti_text[1])
            counter_N += 1

    return pos_list, neg_list


def translate_list(list_to_translate, target_file_name, target_language='en'):
    translated_text = []
    counter = 0
    for text in list_to_translate:
        translated = Sentiment_Analysis_Translate.transalte_text(text, target_language=target_language)
        translated_text.append(translated)
        print(counter)
        counter += 1
    files_api.save_list(translated_text, target_file_name, encoding='utf-8')
    return translated_text


def prepare_eng_lists():
    # English Learning
    eng_pos_list, eng_neg_list = json_reviews_to_list('Data/English/Toys_and_Games_5.json')

    train_eng_pos_list, test_eng_pos_list = seperate_to_train_and_test(eng_pos_list, 0.2)
    train_eng_neg_list, test_eng_neg_list = seperate_to_train_and_test(eng_neg_list, 0.2)
    print("test pos len: {}, train pos len: {}".format(len(test_eng_pos_list), len(train_eng_pos_list)))
    return train_eng_pos_list, train_eng_neg_list, test_eng_pos_list, test_eng_neg_list


def prepare_arabic_lists():
    # Arabic Learning
    arabic_text_list = text_single_file_to_list('Data/Arabic/', 'ar_reviews_100k.tsv', encoding='utf-8')
    pos_arabic, neg_arabic = list_to_pos_neg_arabic(arabic_text_list)
    train_arabic_pos_list, test_arabic_pos_list = seperate_to_train_and_test(pos_arabic, 0.2)
    train_arabic_neg_list, test_arabic_neg_list = seperate_to_train_and_test(neg_arabic, 0.2)
    return train_arabic_pos_list, train_arabic_neg_list, test_arabic_pos_list, test_arabic_neg_list



def run_eng_lexicon(test_eng_pos_list, test_eng_neg_list):
#lexicon_english
    english_results_pos = run_eng_senti(test_eng_pos_list, sentiment="Positive")
    files_api.write_dict_to_csv(english_results_pos, 'lexicon_results_english_pos.csv', encoding=None)

    english_results_neg = run_eng_senti(test_eng_neg_list, sentiment="Negative")
    files_api.write_dict_to_csv(english_results_neg, 'lexicon_results_english_neg.csv', encoding=None)


def run_arabic_lexicon(test_arabic_pos_list, test_arabic_neg_list):
# lexicon_arabic
    arabic_results_pos = run_arabic_senti(test_arabic_pos_list, sentiment="Positive")
    files_api.write_dict_to_csv(arabic_results_pos, 'lexicon_results_arabic_pos.csv', encoding='utf-8')

    arabic_results_neg = run_arabic_senti(test_arabic_neg_list, sentiment="Negative")
    files_api.write_dict_to_csv(arabic_results_neg, 'lexicon_results_arabic_neg.csv', encoding='utf-8')


if __name__ == "__main__":

    # prepare lists
    train_eng_pos_list, train_eng_neg_list, test_eng_pos_list, test_eng_neg_list = prepare_eng_lists()
    train_arabic_pos_list, train_arabic_neg_list, test_arabic_pos_list, test_arabic_neg_list = prepare_arabic_lists()

# Learning
    # eng
    sentiment_analysis_model_run(train_eng_pos_list, train_eng_neg_list, test_eng_pos_list, test_eng_neg_list,
                               file_to_save='learning_eng_result.csv', lang="english", epochs=12)

    # arabic
    sentiment_analysis_model_run(train_arabic_pos_list, train_arabic_neg_list, test_arabic_pos_list, test_arabic_neg_list,
                               file_to_save="learning_arabic_result.csv", epochs=12)


# Lexicon
    run_eng_lexicon(test_eng_pos_list, test_eng_neg_list)
    run_arabic_lexicon(test_arabic_pos_list, test_arabic_neg_list)


# translate
    # translate arabic to english
    #train_translated_arabic_to_eng_neg_list = translate_list(train_arabic_neg_list, 'train_translated_arabic_to_eng_neg_list.txt', target_language='en')
    #train_translated_arabic_to_eng_pos_list = translate_list(train_arabic_pos_list, 'train_translated_arabic_to_eng_pos_list.txt', target_language='en')

    #test_translated_arabic_to_eng_neg_list = translate_list(test_arabic_neg_list, 'test_translated_arabic_to_eng_neg_list.txt', target_language='en')
    #test_translated_arabic_to_eng_pos_list = translate_list(test_arabic_pos_list, 'test_translated_arabic_to_eng_pos_list.txt', target_language='en')

    # learning_translate arabic->english
    train_translated_arabic_to_eng_pos_list = text_single_file_to_list('Data/Arabic/Translated/', 'train_translated_arabic_to_eng_pos_list.txt', encoding='utf-8')
    train_translated_arabic_to_eng_neg_list = text_single_file_to_list('Data/Arabic/Translated/', 'train_translated_arabic_to_eng_neg_list.txt', encoding='utf-8')
    test_translated_arabic_to_eng_pos_list = text_single_file_to_list('Data/Arabic/Translated/', 'test_translated_arabic_to_eng_pos_list.txt', encoding='utf-8')
    test_translated_arabic_to_eng_neg_list = text_single_file_to_list('Data/Arabic/Translated/', 'test_translated_arabic_to_eng_neg_list.txt', encoding='utf-8')

    sentiment_analysis_model_run(train_translated_arabic_to_eng_pos_list, train_translated_arabic_to_eng_neg_list, test_translated_arabic_to_eng_pos_list, test_translated_arabic_to_eng_neg_list,
                                 lang='english', file_to_save='learning_trans_arbic_to_eng_result.csv', epochs=12)

    # lexicon translated arabic -> eng
    arabic_to_english_results_pos = run_eng_senti(test_translated_arabic_to_eng_pos_list, sentiment="Positive")
    files_api.write_dict_to_csv(arabic_to_english_results_pos, 'translated_lexicon_results_arabic_to_english_pos.csv', encoding=None)

    arabic_to_english_results_neg = run_eng_senti(test_translated_arabic_to_eng_neg_list, sentiment="Negative")
    files_api.write_dict_to_csv(arabic_to_english_results_neg, 'translated_lexicon_results_arabic_to_english_neg.csv', encoding=None)


    # translate english to arabic
    #train_translated_eng_to_arabic_neg_list = translate_list(train_eng_neg_list, 'train_translated_eng_to_arabic_neg_list.txt', target_language='ar')
    #train_translated_eng_to_arabic_pos_list = translate_list(train_eng_pos_list, 'train_translated_eng_to_arabic_pos_list.txt', target_language='ar')

    #test_translated_eng_to_arabic_neg_list = translate_list(test_eng_neg_list, 'test_translated_eng_to_arabic_neg_list.txt', target_language='ar')
    #test_translated_eng_to_arabic_pos_list = translate_list(test_eng_pos_list, 'test_translated_eng_to_arabic_pos_list.txt', target_language='ar')

    # learning_translated english->arabic
    #sentiment_analysis_model_run(train_translated_eng_to_arabic_pos_list, train_translated_eng_to_arabic_neg_list, test_translated_eng_to_arabic_pos_list, test_translated_eng_to_arabic_neg_list, file_to_save='learning_trans_eng_to_arabic_result.csv')


    # lexicon translated_eng -> arabic
    #eng_to_arabic_results_pos = run_eng_senti(test_translated_arabic_to_eng_pos_list, sentiment="Positive")
    #files_api.write_dict_to_csv(eng_to_arabic_results_pos, 'translated_lexicon_results_english_to_arabic_pos.csv', encoding='utf-8')

    #eng_to_arabic_results_neg = run_eng_senti(test_translated_arabic_to_eng_neg_list, sentiment="Negative")
    #files_api.write_dict_to_csv(eng_to_arabic_results_neg, 'translated_lexicon_results_aenglish_to_arabic_neg.csv', encoding='utf-8')



