import json


def get_cook_book(filename):
    with open(filename) as fp:
        cook_book = json.load(fp)
        return cook_book


def get_shop_list_by_dishes(dishes, person_count):
    cook_book = get_cook_book('dishes.json')
    shop_list = {}
    for dish in dishes:
        if dish not in cook_book:
            print('Блюдо', dish, 'отсутствует в книге рецептов', '\n')
            continue
        for ingredient in cook_book[dish]:
            new_shop_list_item = dict(ingredient)

            new_shop_list_item['quantity'] *= person_count
            if new_shop_list_item['ingredient_name'] not in shop_list:
                shop_list[new_shop_list_item['ingredient_name']] = new_shop_list_item
            else:
                shop_list[new_shop_list_item['ingredient_name']]['quantity'] += new_shop_list_item['quantity']

    return shop_list


def print_shop_list(shop_list):
    for shop_list_item in shop_list.values():
        print('{} {} {}'.format(shop_list_item['ingredient_name'], shop_list_item['quantity'],
                                shop_list_item['measure']))


def create_shop_list():
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите блюда в расчете на одного человека (через запятую): ') \
        .lower().split(',')
    dishes = list(map(str.strip, dishes))
    shop_list = get_shop_list_by_dishes(dishes, person_count)
    print_shop_list(shop_list)


create_shop_list()
