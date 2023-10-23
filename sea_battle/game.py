from player import AI, User
from board import Board
from dot import Dot
from ship import Ship
from exception import BoardOutException, BoardOccupiedException, BoardRepeatedShotException
import random
import os


class Game:

    def __init__(self):
        self.user = User()
        self.user_board = self.random_board()

        self.ai = AI()
        self.ai_board = self.random_board()

        self.user.own_board, self.ai.enemy_board = (self.user_board,)*2
        self.user.enemy_board, self.ai.own_board = (self.ai_board,)*2

        self.current_player = self.user


    def random_board(self):
        ships = [3, 2, 2, 1, 1, 1, 1]
        attempt = 0

        cursor = 0
        board = Board()

        while True:
            if attempt == 0:
                cursor = 0
                board = Board()

            attempt += 1

            if attempt > 1000:
                attempt = 0
                continue

            ship_size = ships[cursor]

            x = random.randint(1, 6)
            y = random.randint(1, 6)
            direction = random.choice(['horizontal', 'vertical'])
            ship = Ship(ship_size, Dot(x, y), direction)
            try:
                board.add_ship(ship)
            except (BoardOccupiedException, BoardOutException):
                continue

            cursor += 1
            if cursor == len(ships):
                break

        return board

    def switch_players(self):
        self.current_player = self.ai if self.current_player == self.user else self.user

    @staticmethod
    def greet():
        print("Привет!")

    def loop(self):
        while True:
            print("Ваше поле:")
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
                print("Внимательно, капитан, мы уже били по этим координатам!")
            except BoardOutException:
                print("Внимательно, капитан, мы бъем мимо поля!")



    def start(self):
        self.greet()
        self.loop()


if __name__ == "__main__":
    game = Game()
    game.start()

