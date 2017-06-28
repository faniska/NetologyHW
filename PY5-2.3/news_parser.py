import chardet
import os
import json


def read_news_json(file_name):
    folder = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(*[folder, 'data', file_name+'.json'])
    with open(file_path, 'rb') as f:
        data = f.read()
        chardet_result = chardet.detect(data)
        if chardet_result and 'encoding' in chardet_result:
            news_json = data.decode(chardet_result['encoding'])
            news = json.loads(news_json)

            top10 = get_top10_words(news)
            print_top10(top10)


def get_top10_words(news):
    text_fields = ['title', 'description']
    result = {}
    for news_item in news['rss']['channel']['items']:
        for field in text_fields:
            splitted_text = news_item['title'].split()
            for word in splitted_text:
                word = word.lower()
                if len(word) <= 6:
                    continue

                if word not in result:
                    result[word] = 1
                else:
                    result[word] += 1

    sorted(result.values())
    sorted(result, key=result.get)
    sorted_list = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return sorted_list[:10]


def print_top10(words):
    for i, word in enumerate(words):
        print('{}) {} - {}'.format(i + 1, *word))


print('q - выход из программы')

while True:
    input_f = (input('Введите имя файла (без расширения):')).strip()
    if input_f == 'q':
        break
    read_news_json(input_f)
