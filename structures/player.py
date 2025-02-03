from structures.rack import Rack

class Player:
    def __init__(self, name, strategy):
        self.score = 0
        self.rack = Rack()
        self.name = name
        self.strategy = strategy
        self.cant_move = False

    def __str__(self):
        return f"Gracz: {self.name}, Wynik: {self.score}, {self.rack}"