import json
import os.path
import csv

save_path = 'output/'


def write_dict_to_csv(data: list, filename, encoding=None):
    try:
        with open(os.path.join(save_path, filename), mode='w', encoding=encoding) as csv_file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except UnicodeEncodeError:
        with open(os.path.join(save_path, filename), mode='w', encoding='utf-8') as csv_file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

# Saves list to file /n
def save_list(lines, filename, encoding=None):
    data = '\n'.join(lines)
    file = open(os.path.join(save_path, filename), 'w', encoding=encoding)
    file.write(data)
    file.close()


# to load the contents of the file
def load_file(filepath, encoding=None):
    file = open(filepath, 'r', encoding=encoding)  # open the file in the read only mode
    text = file.read()          # read the contents of the file
    file.close()                # close the file
    return text


def load_file_row_to_list(filepath, encoding=None):
    file = open(filepath, 'r', encoding=encoding)  # open the file in the read only mode
    text = file.readlines()         # read the contents of the file
    file.close()                # close the file
    return text


def copy_to_json(data, filename='file', encoding=None):
    with open(os.path.join(save_path, filename), 'w', encoding=encoding) as json_file:
        json.dump(data, json_file)


# to write to the file
def save_list(lines, filename, encoding=None):
    data = '\n'.join(lines)
    try:
        file = open(os.path.join(save_path, filename), 'w', encoding=encoding)
        file.write(data)
        file.close()
    except:
        file = open(os.path.join(save_path, filename), 'w', encoding='utf-8')
        file.write(data)
        file.close()


def save_str_to_text(text, file_name, save_path=save_path):
    with open(os.path.join(save_path, file_name + '.txt'), 'w', encoding='utf-8') as file:
        file.write(text)
