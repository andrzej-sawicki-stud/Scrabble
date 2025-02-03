import random

class Bag:
    def __init__(self):
        self.letters = "AAAAAAAAABBCCDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIJKLLLLMMNNNOOOOOOOOPPQRRRRSSSSTTTUUUUVVWWXYYZ  "
        self._shuffle()

    def _shuffle(self):
        char_list = list(self.letters)
        random.shuffle(char_list)
        self.letters = ''.join(char_list)

    def fill_rack(self, rack):
        n = 7 - len(rack)
        if n >= len(self.letters):
            rack = rack + self.letters
            self.letters = ""
        else:
            rack = rack + self.letters[:n]
            self.letters = self.letters[n:]
        return rack

    def empty(self):
        if not self.letters:
            return True
        return False

    def __str__(self):
        return f"Worek: {len(self.letters)}, Zawartość: {self.letters}"