import random


class BoardOutException(Exception):  # Класс исключения точка вне игрового поля
    pass


class BoardOccupiedException(Exception):  # Класс исключения занятой точки поля
    pass


class BoardRepeatedShotException(Exception):  # Класс исколючения повторный выстрел в одну точку
    pass


class CoordNotValidException(Exception):  # Невалидные координаты введеные игроком
    pass


class Dot:  # Класс точка
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Dot: {self.x, self.y}'


class Ship:  # Класс корабль

    def __init__(self, size, position, direction):
        self.size = size
        self.position = position
        self.direction = direction
        self._hp = size

        self._dots = [self.position]
        if self.direction == "vertical":
            for y in range(position.y + 1, position.y + size):
                self._dots.append(Dot(position.x, y))
        else:
            for x in range(position.x + 1, position.x + size):
                self._dots.append(Dot(x, position.y))

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def dots(self):
        return self._dots


class Board:  # Класс доска
    states = {'empty': ' ', 'ship': '■', 'hit': '□', 'miss': '•'}

    def __init__(self, size, hid=False):
        self.hid = hid
        self.size = size
        self.ship_list = []
        self.field = [[self.states['empty']]*self.size for _ in range(self.size)]

    @property
    def afloat_ships(self):  # Количество кораблей на плаву
        count = 0
        for item_ship in self.ship_list:
            if item_ship.hp > 0:
                count += 1
        return count

    def out(self, dot):  # Точка за пределами доски
        return dot.x > self.size or dot.y > self.size

    def occupied(self, dot):  # Эта точка на доске уже занята
        contoured_dot = self.contour(dot)
        contoured_dot.append(dot)

        for item in contoured_dot:
            if self.field[item.x-1][item.y-1] == self.states['ship']:
                return True

        return False

    def add_ship(self, ship):  # Добавление корабля на доску
        # проверим помещается ли корабль на поле
        for dot in ship.dots:
            if self.out(dot):
                raise BoardOutException
            if self.occupied(dot):
                raise BoardOccupiedException

        # добавим корабль на поле
        for dot in ship.dots:
            self.field[dot.x-1][dot.y-1] = self.states['ship']

        # пополнить список кораблей
        self.ship_list.append(ship)

    def contour(self, element):  # Возвращает список точек вокруг element (Dot или Ship)
        if isinstance(element, Ship):
            dots = element.dots
        else:
            dots = [element]

        contour = []
        for dot in dots:
            for y in range(max(dot.y - 2, 0), dot.y + 1):
                for x in range(max(dot.x - 2, 0), dot.x + 1):
                    check_dot = Dot(x + 1, y + 1)
                    if (check_dot not in dots
                            and check_dot not in contour
                            and x < self.size and y < self.size):
                        contour.append(Dot(x + 1, y + 1))
        return contour

    def show(self):  # Вывод доски на экран
        for y in range(self.size + 1):
            for x in range(0, self.size + 1):
                if x == 0 and y == 0:
                    print(f"{' ':^2}", end='')
                elif x == 0:
                    print(f"{y:^2}", end='')
                elif y == 0:
                    print(f"{x:^2}", end='' if x < self.size else None)
                else:
                    point = self.field[x-1][y-1]
                    if self.hid and point not in (self.states['hit'], self.states['miss']):
                        point = self.states['empty']

                    print(f"{point:^2}", end='' if x < self.size else None)

    def shot(self, dot):  # Выстрел по доске
        if self.out(dot):
            raise BoardOutException

        state = self.field[dot.x - 1][dot.y - 1]
        if state in (self.states['miss'], self.states['hit']):  # Сюда уже били
            raise BoardRepeatedShotException

        if state == self.states['empty']:
            self.field[dot.x - 1][dot.y - 1] = self.states['miss']  # Промазали
            print('Мимо!')
            return False

        if state == self.states['ship']:  # Попали по кораблю
            self.field[dot.x - 1][dot.y - 1] = self.states['hit']
            item_ship = self.ship_by_dot(dot)
            item_ship.hp -= 1
            if item_ship.hp == 0:
                print('Корабль уничтожен!')
                ship_contour = self.contour(item_ship)
                for item in ship_contour:
                    self.field[item.x - 1][item.y - 1] = self.states['miss']
            else:
                print('Корабль ранен!1')
            return True

    def ship_by_dot(self, dot):  # Получение корабля по точке
        for item_ship in self.ship_list:
            if dot not in item_ship.dots:
                continue
            return item_ship


class Player:  # Класс игрок

    own_board = None
    enemy_board = None

    def ask(self):
        pass

    def move(self):
        dot = self.ask()
        return self.enemy_board.shot(dot)


class AI(Player):  # Класс ИИ

    def ask(self):
        x = random.randint(1, self.enemy_board.size)
        y = random.randint(1, self.enemy_board.size)
        return Dot(x, y)


class User(Player):  # Класс пользователь ПК
    def ask(self):
        result = input("Введите значение координаты х,y: ").split(",")
        result = list(filter(self.correct_coordinates, result))
        if len(result) != 2:
            raise CoordNotValidException

        x, y = map(int, result)
        return Dot(x, y)

    @staticmethod
    def correct_coordinates(coord):
        coord = coord.strip()
        if not coord:
            return False
        if not coord.isdecimal():
            return False
        return True


class Game:
    board_size = 6  # Размер доски
    ships = [3, 2, 2, 1, 1, 1, 1]  # Типы кораблей на доске

    def __init__(self):
        self.user = User()
        self.user_board = self.random_board()

        self.ai = AI()
        self.ai_board = self.random_board(True)

        self.user.own_board, self.ai.enemy_board = (self.user_board,)*2
        self.user.enemy_board, self.ai.own_board = (self.ai_board,)*2

        self.current_player = self.user

    def random_board(self, hid=False):  # Установка кораблей на доске
        attempt = 0

        cursor = 0
        board = Board(self.board_size, hid)

        while True:
            if attempt == 0:
                cursor = 0
                board = Board(self.board_size, hid)

            attempt += 1

            if attempt > 1000:
                attempt = 0
                continue

            ship_size = self.ships[cursor]

            x = random.randint(1, self.board_size)
            y = random.randint(1, self.board_size)
            direction = random.choice(['horizontal', 'vertical'])
            ship = Ship(ship_size, Dot(x, y), direction)
            try:
                board.add_ship(ship)
            except (BoardOccupiedException, BoardOutException):
                continue

            cursor += 1
            if cursor == len(self.ships):
                break

        return board

    def switch_players(self):  # Смена текущего игрока
        self.current_player = self.ai if self.current_player == self.user else self.user

    @staticmethod
    def greet():
        print("Привет, капитан, мы тебя ждали, пора сразиться в морской бой.")

    def loop(self):
        while True:
            print("Наше поле:")
            self.user.own_board.show()
            print("Поле противника:")
            self.ai.own_board.show()

            if self.user.enemy_board.afloat_ships == 0:
                print("Поздравляю, капитан, мы уничтожили флот противника!")
                break

            if self.user.own_board.afloat_ships == 0:
                print("Увы, капитан, противник уничтожил наш флот!")
                break

            try:
                if not self.current_player.move():
                    self.switch_players()
            except BoardRepeatedShotException:
                if self.current_player == self.user:
                    print("Внимательно, капитан, мы уже били по этим координатам!")
            except BoardOutException:
                if self.current_player == self.user:
                    print("Внимательно, капитан, мы бъем мимо поля!")
            except CoordNotValidException:
                if self.current_player == self.user:
                    print("Капитан, ваш приказ не понятен!")

    def start(self):
        self.greet()
        self.loop()


Game().start()
