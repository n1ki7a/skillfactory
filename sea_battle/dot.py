class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Dot: {self.x, self.y}'


if __name__ == "__main__":
    dot1 = Dot(1, 1)
    dot2 = Dot(2, 1)
    print(dot1)
    print(dot2)
