import glob
import requests
import os

API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate_it(input_file, output_file, from_lang, to_lang):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param input_file: 
    :param output_file: 
    :param from_lang: 
    :param to_lang: 
    :return: 
    """

    text = read_input_file_content(input_file)

    params = {
        'key': API_KEY,
        'text': text,
        'lang': '{}-{}'.format(from_lang, to_lang),
    }
    response = requests.get(URL, params=params)
    result = response.json()
    save_result_to_file(output_file, result['text'])


def save_result_to_file(output_file, text):
    mode = 'w' if os.path.exists(output_file) else 'x'
    with open(output_file, mode) as output_file_stream:
        output_file_stream.write(''.join(text))


def read_input_file_content(input_file):
    if not os.path.exists(input_file):
        return ''
    with open(input_file) as input_file_content:
        return input_file_content.read()


def translate_all_files():
    files = glob.glob('./input/*.txt')
    for file in files:
        basename = os.path.basename(file)
        filename = os.path.splitext(basename)
        from_lang = filename[0].lower()
        output_file = './output/{}-{}.txt'.format(from_lang, 'ru')
        translate_it(file, output_file, from_lang, 'ru')


translate_all_files()
