
class Player:

    def __init__(self):
        self.own_board = Board()
        self.enemy_board = Board()

    def ask(self):
        pass

    def move(self):
        dot = self.ask()
