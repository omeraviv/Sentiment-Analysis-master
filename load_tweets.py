import json
import os.path
from os import listdir
from files_api import save_str_to_text
import files_api


def js_r(filename, original_tweets_data_path):
   with open(os.path.join(original_tweets_data_path, filename), 'r') as file:
       return(json.load(file))

def save_tweets_to_text_files(original_tweets_data_path):
    for filename in listdir(original_tweets_data_path):
        text_list = []
        counter = 0
        tweet = js_r(filename, original_tweets_data_path)
        if tweet['raw_data']['truncated']:
            text = tweet['raw_data']['extended_tweet']['full_text']
        else:
            text = tweet['raw_data']['text']
        text_list.append([text, counter])
        save_str_to_text(text, filename, save_path="Data/tweets.Text/")
        for child in tweet['children'].values():
            if child['raw_data']['truncated']:
                child_text = child['raw_data']['extended_tweet']['full_text']
            else:
                child_text = child['raw_data']['text']
            # check if the original text of the tweet is copied to the child tweet
#            index = child_text.find(text)
 #           if index != -1:
            child_text.replace(text, "")
            if child_text not in text_list:
                text_list.append([child_text, counter])
            counter += 1
        for [text,counter] in text_list:
            save_str_to_text(text, filename + str(counter), save_path="Data/tweets.Text/")


def save_tweets_to_text_files2(original_tweets_data_path):
    tweets = files_api.load_file_row_to_list(os.path.join(original_tweets_data_path, 'ar_reviews_100k.tsv'), encoding='utf-8')
    counter = 0
    for tweet in tweets:
        if len(tweet.split()) > 100:
            save_str_to_text(tweet, 'tweet' + str(counter), save_path="Data/tweets.Text/")
            counter += 1



