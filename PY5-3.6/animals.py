class Animals:
    warm_blooded = None  # Теплокровные
    vertebrates = None  # Позвоночные
    cover = None  # Покров
    color = None  # Цвет
    weight = 0  # Вес в кг
    name = ''

    def __init__(self, name, color, weight):
        self.name = name
        self.color = color
        self.weight = weight
        print(self.name)

    def make_sound(self):
        print('Издает звук')

    def move(self):
        print('Передвигается')

    def eat(self):
        print('Ест')


class Birds(Animals):
    warm_blooded = True
    vertebrates = True
    cover = 'Перья'
    can_fly = True
    can_swim = False

    def fly(self):
        if self.can_fly:
            print('Летает')
        else:
            print('Не летает')

    def swim(self):
        if self.can_swim:
            print('Плавает')
        else:
            print('Не плавает')


class Mammals(Animals):
    warm_blooded = True
    vertebrates = True
    cover = 'Шерсть'


class Cow(Mammals):
    def make_sound(self):
        super(Cow, self).make_sound()
        print('Му-у-у')


class Goose(Birds):
    can_swim = True

    def make_sound(self):
        super(Goose, self).make_sound()
        print('Га-га-га')


class Сhicken(Birds):
    def make_sound(self):
        super(Сhicken, self).make_sound()
        print('Ко-ко-ко')


cow = Cow('корова', 'черно-белая', 720)
cow.make_sound()

print('-----')

goose = Goose('гусь', 'белый', 3)
goose.swim()
goose.make_sound()

print('-----')

chicken = Сhicken('курица', 'коричневая', 1)
chicken.swim()
chicken.make_sound()