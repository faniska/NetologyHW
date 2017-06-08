documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]
directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def get_available_commands():
    available_commands = {
        'p': {'command': get_person,
              'help': 'people – команда, которая спросит номер документа и выведет имя человека, '
                      'которому он принадлежит'},
        'l': {'command': print_list, 'help': 'list – команда, которая выведет список всех документов'},
        's': {'command': get_shelf,
              'help': 'shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится'},
        'a': {'command': add_document,
              'help': 'add – команда, которая добавит новый документ в каталог и в перечень полок, '
                      'спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться'},
        'h': {'command': print_help, 'help': 'help - показывает справочник доступных команд'},
        'q': {'command': exit, 'help': 'quit - выход из программы'},
        'd': {'command': delete_document, 'help': 'delete – команда, которая спросит номер документа и '
                                                  'удалит его из каталога и из перечня полок;'}
    }
    return available_commands


def directory_helper():
    available_commands = get_available_commands()
    print("\n-----\n")
    command = input('Введите команду (h для справки): ')
    if command in available_commands:
        print("\n-----\n")
        res = available_commands[command]['command']()
        if res:
            print(res)
    else:
        print('Такой команды нет. Введите h, чтобы получить список доступных комманд. Либо q, чтобы выйти из программы')


def print_help():
    available_commands = get_available_commands()
    for key, command in available_commands.items():
        print(key, '-', command['help'])


def ask_document_number():
    return input('Введите номер документа: ')


def get_person():
    number = ask_document_number()
    for document in documents:
        if document['number'] == number:
            return document['name']


def print_list():
    for document in documents:
        print('{0} "{1}" "{2}"'.format(document['type'], document['number'], document['name']))


def get_shelf():
    number = ask_document_number()
    for index, directory in directories.items():
        if number in directory:
            return 'Указанный документ лежит на полке под номером ' + index
    return 'Программа не нашла документ с таким номером. ' \
           'Введите l, чтобы отобразить список доступных документов'


def add_document():
    doc_number = ask_document_number()
    while is_document_in_directory(doc_number):
        print('Документ с таким номером уже есть каталоге')
        doc_number = ask_document_number()

    doc_type = input('Введите тип документа: ')
    doc_owner = input('Введите имя владельца: ')

    if doc_number and doc_number and doc_owner:
        new_document = {
            'type': doc_type,
            'number': doc_number,
            'name': doc_owner
        }

        documents.append(new_document)
        print('Документ успешно добавлен', "\n", '-----', "\n")

        while add_document_to_shelf(doc_number) is not True:
            continue


def is_document_in_directory(doc_number):
    return any(document['number'] == doc_number for document in documents)


def delete_document():
    doc_number = ask_document_number()
    if is_document_in_directory(doc_number) is not True:
        return 'Документ с указанным номером не найден в каталоге'
    delete_doc_from_shelves(doc_number)
    delete_doc_from_directory(doc_number)


def delete_doc_from_shelves(doc_number):
    for shelf, doc_numbers in directories.items():
        if doc_number not in doc_numbers:
            continue
        index = doc_numbers.index(doc_number)
        del doc_numbers[index]
        print('Документ удален из полки каталога')


def delete_doc_from_directory(doc_number):
    for index, document in enumerate(documents):
        if document['number'] == doc_number:
            del documents[index]
            print('Документ с указанным номером удален из каталога')


def add_document_to_shelf(doc_number):
    shelves_numbers = list(directories.keys())
    shelves_numbers.sort()
    available_shelves = ', '.join(shelves_numbers)
    shelf_number = input('Введите номер полки (' + available_shelves + '): ')
    if shelf_number in directories:
        directories[shelf_number].append(doc_number)
        print('Документ размещен на полке под номером', shelf_number)
        return True

    print('К сожалению нет полки под номером', shelf_number)


while True:
    directory_helper()
