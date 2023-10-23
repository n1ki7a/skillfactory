from dot import Dot
from ship import Ship
from exception import BoardOutException, BoardOccupiedException, BoardRepeatedShotException


class Board:
    _width = 6
    _height = 6
    _ships = [3, 2, 2, 1, 1, 1, 1]
    states = {'empty': ' ', 'ship': '■', 'hit': '□', 'miss': '•'}

    def __init__(self, hid):
        self.hid = hid
        self.ship_list = []
        self.field = [[self.states['empty']]*self._width for _ in range(self._height)]

    @property
    def afloat_ships(self):
        count = 0
        for item_ship in self.ship_list:
            if item_ship.hp > 0:
                count += 1
        return count

    def out(self, dot):
        return dot.x > self._width or dot.x > self._height

    def occupied(self, dot):
        contoured_dot = self.contour(dot)
        contoured_dot.append(dot)

        for item in contoured_dot:
            if self.field[item.x-1][item.y-1] == self.states['ship']:
                return True

        return False

    def add_ship(self, ship):
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

    def contour(self, element):
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
                            and x < self._width and y < self._height):
                        contour.append(Dot(x + 1, y + 1))
        return contour

    def show(self):
        for y in range(self._height + 1):
            for x in range(0, self._width + 1):
                if x == 0 and y == 0:
                    print(f"{' ':^2}", end='')
                elif x == 0:
                    print(f"{y:^2}", end='')
                elif y == 0:
                    print(f"{x:^2}", end='' if x < self._width else None)
                else:
                    point = self.field[x-1][y-1]

                    print(f"{point:^2}", end='' if x < self._width else None)

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException

        state = self.field[dot.x - 1][dot.y - 1]
        if state in (self.states['miss'], self.states['hit']):
            raise BoardRepeatedShotException

        if state == self.states['empty']:
            self.field[dot.x - 1][dot.y - 1] = self.states['miss']
            return False

        if state == self.states['ship']:
            self.field[dot.x - 1][dot.y - 1] = self.states['hit']
            item_ship = self.ship_by_dot(dot)
            item_ship.hp -= 1
            if item_ship.hp == 0:
                print('Корабль уничтожен')
                ship_contour = self.contour(item_ship)
                for item in ship_contour:
                    self.field[item.x - 1][item.y - 1] = self.states['miss']
            else:
                print('Корабль ранен')
            return True


    def ship_by_dot(self, dot):
        for item_ship in self.ship_list:
            if dot not in item_ship.dots:
                continue
            return item_ship


if __name__ == "__main__":
    board = Board(False)

    ship = Ship(3, Dot(2,3), 'h')
    board.add_ship(ship)

    ship = Ship(2, Dot(6,1), 'v')
    board.add_ship(ship)

    print(board.afloat_ships)
    board.shot(Dot(2, 3))
    board.shot(Dot(3, 3))
    print(board.afloat_ships)
    board.shot(Dot(4, 3))

    print(board.afloat_ships)
    board.shot(Dot(6, 1))
    board.shot(Dot(6, 2))
    print(board.afloat_ships)
    board.show()

