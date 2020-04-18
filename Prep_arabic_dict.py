import csv
import os.path


def load_file(filepath, encoding='utf-8'):
    file = open(filepath, 'r', encoding=encoding)  # open the file in the read only mode
    text = file.read()          # read the contents of the file
    file.close()                # close the file
    return text


def read_csv_to_dict(filename, encoding='utf-8') -> dict:
    with open(filename, encoding=encoding, newline='') as file:
        reader = csv.reader(file)
        results = dict(reader)
        for key in results.keys():
            if results[key] == 'Negative' or results[key] == ' Negative':
                results[key] = -0.2
            elif results[key] == 'Strong Negative' or results[key] == ' Strong Negative':
                results[key] = -1

            elif results[key] == 'Positive' or results[key] == ' Positive':
                results[key] = 0.2
            elif results[key] == 'Strong Positive' or results[key] == ' Strong Positive':
                results[key] = 1
            else:
                results[key] = 0
    return results

# not used. created for old dict i used.
def encode_arabic_dict(filepath, encoding):
    dict_str = load_file(filepath, encoding)
    lines = dict_str.split("\n")
    arab_dict = {}
    for line in lines:
        line_list = line.split('\t')
        if len(line_list) < 5:
            continue
        senti = float(line_list[2])
        senti = senti / 2.5
        if senti > 1:
            senti = 1
        elif senti < -1:
            senti = -1
        arab_dict[line_list[0]] = senti
    return arab_dict


# to write to the file
def save_list(lines, filename, encoding):
    data = [str(word) + str(senti) for word, senti in lines.items()]
    data = '\n'.join(data)
    file = open(filename, 'w', encoding=encoding)
    file.write(data)
    file.close()


def file_to_senti_dict(data_path):
    lexi = {}
    with open(os.path.join(data_path, 'Pos.txt'), 'r', encoding='utf-8') as pf:
        pos_words = pf.read().split('\n')
    with open(os.path.join(data_path, 'Neg.txt'), 'r', encoding='utf-8') as nf:
        neg_words = nf.read().split('\n')
    for word in pos_words:
        lexi[word] = 1
    for word in neg_words:
        lexi[word] = -1
    return lexi


if __name__ == '__main__':



    # arab_dict = encode_arabic_dict("Arabic_Emoticon_Lexicon.txt", 'utf-8')
    # save_list(arab_dict, 'arab.txt', encoding='utf-8')

    lexi = read_csv_to_dict('arabic_lexi.csv')
    #for key, senti in lexi.items():
     #   print("word is: {} lexi is: {}".format(key, senti))