class Board:
    def __init__(self):
        self.grid = [[None for _ in range(15)] for _ in range(15)]

    def get(self):
        return self.grid

    def put_word(self, word, position, vertical):
        x, y = position
        if vertical:
            for letter in word:
                self.grid[x][y] = letter
                y = y + 1
        else:
            for letter in word:
                self.grid[x][y] = letter
                x = x + 1

    def __str__(self):
        text = ""
        for row in self.grid:
            text = text + " ".join(cell if cell is not None else "." for cell in row) + "\n"
        return text[:-1]