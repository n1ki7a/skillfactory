from board import Board
from dot import Dot
import random


class Player:

    def __init__(self):
        self.own_board = Board()
        self.enemy_board = Board(True)

    def ask(self):
        pass

    def move(self):
        dot = self.ask()
        return self.enemy_board.shot(dot)


class AI(Player):

    def ask(self):
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        return Dot(x, y)


class User(Player):
    def ask(self):
        x = int(input("Введите значение координаты х: "))
        y = int(input("Введите значение координаты у: "))
        return Dot(x, y)
