import files_api
import os.path

def prepare_words_file(file_path):
    words_list = []
    with open(os.path.join(file_path, 'more_positive.txt'), 'r') as f:
        words = f.read()
        words = words.split('\n')
        for line in words:
            words_in_line = line.split('\t')
            for word in words_in_line:
                words_list.append(word)
    with open(os.path.join(file_path, 'new_positive.txt'), 'w') as f2:
        for single_word in words_list:
            f2.write(single_word + '\n')


prepare_words_file('lexicon/')