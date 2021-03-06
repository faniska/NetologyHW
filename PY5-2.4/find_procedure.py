# заготовка для домашней работы
# прочитайте про glob.glob
# https://docs.python.org/3/library/glob.html

# Задание
# мне нужно отыскать файл среди десятков других
# я знаю некоторые части этого файла (на память или из другого источника)
# я ищу только среди .sql файлов
# 1. программа ожидает строку, которую будет искать (input())
# после того, как строка введена, программа ищет её во всех файлах
# выводит список найденных файлов построчно
# выводит количество найденных файлов
# 2. снова ожидает ввод
# поиск происходит только среди найденных на этапе 1
# 3. снова ожидает ввод
# ...
# Выход из программы программировать не нужно.
# Достаточно принудительно остановить, для этого можете нажать Ctrl + C

# Пример на настоящих данных

# python3 find_procedure.py
# Введите строку: INSERT
# ... большой список файлов ...
# Всего: 301
# Введите строку: APPLICATION_SETUP
# ... большой список файлов ...
# Всего: 26
# Введите строку: A400M
# ... большой список файлов ...
# Всего: 17
# Введите строку: 0.0
# Migrations/000_PSE_Application_setup.sql
# Migrations/100_1-32_PSE_Application_setup.sql
# Всего: 2
# Введите строку: 2.0
# Migrations/000_PSE_Application_setup.sql
# Всего: 1

# не забываем организовывать собственный код в функции
# на зачёт с отличием, использовать папку 'Advanced Migrations'

import glob
import os

migrations = 'Migrations'


def init_search(files, placeholder='Введите искомое слово:'):
    print('- - - - - -')
    founded_files = []
    search = input(placeholder).strip()
    for file in files:
        with open(file) as f:
            content = f.read()
            if search.lower() not in content.lower():
                continue
            print(file)
            founded_files.append(file)
    count = len(founded_files)

    if count > 0:
        print('Всего: {}'.format(count))
        init_search(founded_files, 'Введите слово, чтобы искать по найденным файлам:')
    else:
        print('Не удалось найти файлы по введенному ключевому слову')
        init_search(files)

files = []
scan = os.scandir(migrations)
for entry in scan:
    filename, file_extension = os.path.splitext(entry.path)
    if entry.is_file() and file_extension.lower() == '.sql':
        files.append(entry.path)

init_search(files)
