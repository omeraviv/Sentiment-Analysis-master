import senticnet5


def check_dict(dict_to_check = senticnet5.senticnet):
    negative = 0
    positive = 0
    for word in dict_to_check.keys():
        senti = dict_to_check[word][7]
        if float(senti) < -0.75:
            negative +=1
        else:
            positive +=1

    print(positive/(positive+negative))


def create_git_ignore_file():
    with open('. gitignore', 'w') as f:
        f.write('**/Data')


print(check_dict())