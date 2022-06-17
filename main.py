import requests as req
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_content(url):
    return req.get(url,
                   params={"action": "query", "prop": "extracts", "titles": "Ozone_layer", "format": "json"}).json()


def clean_data(data):
    data = data['query']['pages']['22834']['extract']
    regex = re.compile('<.*?>')
    data = re.sub(regex, '', data)
    # return re.split("\. |, |\. |\n |- |\'", data)
    data = data.replace(",", "").replace(",", "")
    return data.split()


def lower_collection(data):
    lower_data = [i.lower() for i in data]
    return lower_data


def tokenize(data):
    not_isalnum_words_list = [i for i in data if i.isalnum()]
    clean_num_list = [i for i in not_isalnum_words_list if not i.isdigit()]
    clean_list = [i for i in clean_num_list if not len(i) < 3]
    return clean_list


def data_full_cleaner(data):
    stop_words = ['and', 'the', 'was', 'were', 'that', 'this', 'for', 'who', 'where', 'into', 'can', 'then', 'are',
                  'more', 'than', 'less', 'these', 'until', 'out', 'from', 'about', 'have', 'has', 'which', 'with',
                  'over']
    l = [i for i in data if not i in stop_words]

    d = {}
    for i in l:
        d[i] = l.count(i)

    data = pd.Series(d).reset_index()
    data.columns = ['name', 'num']
    data = data.sort_values(by='num', ascending=False)
    return data[:20]


def visualition(data):
    sns.barplot(x="num", y="name", data=data)
    plt.show()


def main():
    json_data = get_content("https://en.wikipedia.org/w/api.php")
    cleaned_data = clean_data(json_data)
    lower_data = lower_collection(cleaned_data)
    clean_list = tokenize(lower_data)
    data = data_full_cleaner(clean_list)
    visualition(data)


main()
