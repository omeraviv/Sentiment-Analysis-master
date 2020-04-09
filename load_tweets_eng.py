import json
import os.path
from os import listdir
from files_api import save_str_to_text
import files_api

original_tweets_data_path = 'Data/myData/'
neg_save_path = 'neg_files/'
pos_save_path = 'pos_files/'

def save_tweets_to_text_files_eng(original_tweets_data_path, save_path, senti, senti_path):
    tweets = files_api.load_file_row_to_list(os.path.join(original_tweets_data_path, senti))
    counter = 0
    for tweet in tweets:
        save_str_to_text(tweet, 'tweet' + str(counter), save_path=os.path.join(save_path, senti_path))
        counter += 1



save_tweets_to_text_files_eng(original_tweets_data_path, save_path=original_tweets_data_path, senti='positive.txt', senti_path=pos_save_path)
save_tweets_to_text_files_eng(original_tweets_data_path, save_path=original_tweets_data_path, senti='negative.txt', senti_path=neg_save_path)