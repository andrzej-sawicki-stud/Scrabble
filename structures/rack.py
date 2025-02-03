from algorithms.scrabble import get_letter_value

class Rack:
    def __init__(self):
        self.letters = ""

    def value(self):
        score = 0
        for letter in self.letters:
            score = score + get_letter_value(letter)
        return score

    def empty(self):
        if not self.letters:
            return True
        return False

    def get(self):
        return self.letters

    def __str__(self):
        return f"Stojak: {self.letters}"