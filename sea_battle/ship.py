from dot import Dot


class Ship:

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


if __name__ == "__main__":

    ship = Ship(2, Dot(1,3), "vertical")
    for dot in ship.dots:
        print(dot)
