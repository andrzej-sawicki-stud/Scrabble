import pickle

def get_letter_value(letter):
    letter_values = {
        "A": 1, "E": 1, "I": 1, "L": 1, "N": 1, "O": 1, "R": 1, "S": 1, "T": 1, "U": 1,
        "D": 2, "G": 2,
        "B": 3, "C": 3, "M": 3, "P": 3,
        "F": 4, "H": 4, "V": 4, "W": 4, "Y": 4,
        "K": 5,
        "J": 8, "X": 8,
        "Q": 10, "Z": 10
    }
    return letter_values.get(letter.upper(), 0)

def get_premium_word_value(x, y):
    premium_word_positions = {
        (0, 0): 3, (0, 7): 3, (0, 14): 3,
        (7, 0): 3, (7, 14): 3,
        (14, 0): 3, (14, 7): 3, (14, 14): 3,
        (1, 1): 2, (2, 2): 2, (3, 3): 2, (4, 4): 2,
        (10, 10): 2, (11, 11): 2, (12, 12): 2, (13, 13): 2,
        (1, 13): 2, (2, 12): 2, (3, 11): 2, (4, 10): 2,
        (10, 4): 2, (11, 3): 2, (12, 2): 2, (13, 1): 2,
        (7, 7): 2,
    }
    return premium_word_positions.get((x, y), 1)

def get_premium_letter_value(x, y):
    premium_letter_positions = {
        (0, 3): 2, (0, 11): 2,
        (2, 6): 2, (2, 8): 2,
        (3, 0): 2, (3, 7): 2, (3, 14): 2,
        (6, 2): 2, (6, 6): 2, (6, 8): 2, (6, 12): 2,
        (7, 3): 2, (7, 11): 2,
        (8, 2): 2, (8, 6): 2, (8, 8): 2, (8, 12): 2,
        (11, 0): 2, (11, 7): 2, (11, 14): 2,
        (14, 3): 2, (14, 11): 2,
        (1, 5): 3, (1, 9): 3,
        (5, 1): 3, (5, 13): 3,
        (9, 1): 3, (9, 13): 3,
        (13, 5): 3, (13, 9): 3
    }
    return premium_letter_positions.get((x, y), 1)

class Node:
    def __init__(self):
        self.edges = {}
        self.set = []

class Scrabble:
    def __init__(self, filename):
        self.root = Node()
        """
        Autorska implementacja algorytmu z artykułu naukowego
        "A Faster Scrabble Move Generation Algorithm"
        SOFTWARE—PRACTICE AND EXPERIENCE, VOL. 24(2), 219–232 (FEBRUARY 1994)
        Pseudokod algorytmu znajduje się na stronie nr 7
        """
        def add_semi_minimized(word):
            def add_arc(st, ch):
                if ch not in st.edges:
                    st.edges[ch] = Node()
                return st.edges[ch]

            def add_final_arc(st, c1, c2):
                st = add_arc(st, c1)
                st.set.append(c2)
                return st

            def force_arc(st, ch, fst):
                if ch in st.edges and st.edges[ch] != fst:
                    raise ValueError("an error occurs if an arc from st for ch already exists going to any other state")
                elif ch not in st.edges:
                    st.edges[ch] = fst

            st = self.root
            for i in range(len(word) - 1, 1, -1):
                st = add_arc(st, word[i])
            st = add_final_arc(st, word[1], word[0])

            st = self.root
            for i in range(len(word) - 2, -1, -1):
                st = add_arc(st, word[i])
            st = add_final_arc(st, "|", word[len(word) - 1])

            for m in range(len(word) - 3, -1, -1):
                forceSt = st
                st = self.root
                for i in range(m, -1, -1):
                    st = add_arc(st, word[i])
                st = add_arc(st, "|")
                force_arc(st, word[m + 1], forceSt)

        with open(filename, 'r') as file:
            for line in file:
                word = line.strip().upper() # w grze posługuję się wielkimi literami
                add_semi_minimized(word)

    def find_all_moves(self, board, rack):
        rack = ''.join(sorted(rack)) # posortuj litery na stojaku


        def get_interesting_positions_horizontally(board):
            """
            Własna implementacja wyszukiwania pozycji kotwiczących
            Znajdź ostatnią literę ułożonego słowa oraz takie pozycje, które są puste i mają sąsiadów wertykalnych
            oraz nie mają sąsiada po prawej stronie

            Przedstawiona implementacja różni się od pomysłu przedstawionego przez autora, jednakże jest jedyną
            poprawnie działajacą implementacją zgodną z pseudokodem generacji ruchu przedstawioną przez autora.
            Autor w artykule zasugerował generacje ruchu od pustych sąsiednich pozycji od słów z lewej lub prawej
            strony. Jednakże, zaimplementowanie tego w ten sposób powoduje redundancje wyników generacji i nieoptymalne,
            kosztowne wywołania dla każdej jednej litery na stojaku. Dzięki uznania pozycji kotwiczących na najbardziej
            prawej literze słowa zaproponowany w artykule pomysł najpierw wchłania wszystkie litery istniejącego słowa
            a dopiero następnie iteruje po każdej jednej literze w stojaku wyszukując wszystkich możliwych poprawnych
            kombinacji literek przechodząc po grafie GADDAG. Wynikają z tego znaczne korzyści wydajnościowe.

            "A Faster Scrabble Move Generation Algorithm"
            SOFTWARE—PRACTICE AND EXPERIENCE, VOL. 24(2), 219–232 (FEBRUARY 1994)
            Niezrealizowany pomysł znajduje się na stronie 5, przedostatnim paragrafie
            """
            positions = []
            for y in range(15):
                for x in range(15):
                    if (
                        board[x][y] and x == 15 or
                        board[x][y] and x + 1 < 15 and not board[x + 1][y] or
                        (not board[x][y] and y + 1 < 15 and board[x][y + 1] or
                            not board[x][y] and y - 1 >= 0 and board[x][y - 1]) and
                            (x + 1 < 15 and not board[x + 1][y] or x + 1 >= 15) and
                            ((x - 1 >= 0 and not board[x - 1][y]) and
                            (x - 2 >= 0 and not board[x - 2][y] or x - 2 < 0) or
                            (x - 1 >= 0 and not board[x - 1][y] or x - 1 < 0) and
                            (x + 2 < 15 and not board[x + 1][y] or x + 2 >= 15))
                    ):
                        if (x - 1, y) not in positions:
                            positions.append((x, y))
            return positions

        """
        Autorska implementacja algorytmu z artykułu naukowego
        "A Faster Scrabble Move Generation Algorithm"
        SOFTWARE—PRACTICE AND EXPERIENCE, VOL. 24(2), 219–232 (FEBRUARY 1994)
        Pseudokod algorytmu znajduje się na stronie nr 6
        Różnice w implementacji w stosunku do pseudokodu zostały opatrzone komentarzem
        
        Do algorytmu dodano dwie optymalizacje, które powodują, że generowane są słowa bez powtórzeń. Zostało
        to osiągnięte dzięki wprowadzeniu poprawki do funkcji gen w postaci iteracji po literach bez powtórzeń,
        dla przypadków powtórzeń tych samych liter w stojaku oraz dla mydełka, by nie sprawdzało tych liter, które
        wcześniej zostały sprawdzone podczas iteracji po literach w stojaku, ponieważ się w nim znajdowały
        """
        pos1, pos2 = 0, 0 # modyfikacja, autor przewidywał jedynie przypadek jednowymiarowej tabeli, wprowadzenie drugiej współrzędnej
        results = [] # modyfikacja

        def no_duplicates_and_blanks(rack):
            """
            Usuwa duplikaty liter oraz mydełka
            :param rack: Stojak, string
            :return: Przygotowany ciąg znaków
            """
            result = []
            for i in range(len(rack)):
                if i == 0 or rack[i] != rack[i - 1] and rack[i] != " ":
                    result.append(rack[i])
            return ''.join(result)

        def letters_for_blank(rack):
            """
            Usuwa ze wszystkich liter te litery, które znajdują się w stojaku
            :param rack: Stojak, string
            :return: Przygotowany ciąg znaków
            """
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for letter in rack:
                letters = letters.replace(letter, '', 1)
            return letters

        def allowed(pos, letters):
            if not crosschecks[pos1 + pos][pos2]:
                return letters
            else:
                letters = list(set(crosschecks[pos1 + pos][pos2]) & set(letters))
                return ''.join(letters)

        def gen(pos, word, rack, arc, save=False):
            if L := get_letter_at_pos(pos):
                go_on(pos, L, word, rack, NextArc(arc, L), arc, save)
            elif rack:
                for L in allowed(pos, no_duplicates_and_blanks(rack)): # optymalizacja, nie ma sensu sprawdzać kilka razy tej samej litery dla danej pozycji jeśli kilka takich samych liter znajduje się w stojaku
                    go_on(pos, L, word, rack.replace(L, '', 1), NextArc(arc, L), arc, True)
                if " " in rack:
                    for L in allowed(pos, letters_for_blank(no_duplicates_and_blanks(rack))): # optymalizacja, nie ma sensu testować tej samej litery, która już została przetestowana w pętli wyżej, bo znajdowała się na stojaku
                        if L not in rack:
                            go_on(pos, L, word, rack.replace(" ", '', 1), NextArc(arc, L), arc, True)

        def go_on(pos, L, word, rack, new_arc, old_arc, save):
            if pos <= 0:
                word = L + word
                if L in old_arc.set and no_letter_to_left(pos) and save: RecordPlay(word, pos)
                if new_arc:
                    if has_room_to_left(pos): gen(pos - 1, word, rack, new_arc)
                    new_arc = NextArc(new_arc, "|")
                    if new_arc and no_letter_to_left(pos) and has_room_to_right(0):
                        gen(1, word, rack, new_arc, save)
            elif pos > 0:
                word = word + L
                if L in old_arc.set and no_letter_to_right(pos) and save: RecordPlay(word, pos)
                if new_arc and has_room_to_right(pos):
                    gen(pos + 1, word, rack, new_arc, save)

        # -------- pomocnicze funkcje

        def NextArc(arc, letter):
            if letter in arc.edges:
                return arc.edges[letter]
            return None

        def RecordPlay(word, pos): # autor artykułu nie opisał, jak ta funkcja miałaby działać, implementacja własna
            """
            Algorytm zaproponowany przez autora w artykule rozróżnia litery,
            :param word:
            :param pos:
            """
            x = -1
            y = pos2
            if pos <= 0:
                x = pos1 + pos
            elif pos > 0:
                x = pos1 + pos - len(word) + 1
            if vertical:
                x, y = y, x
            results.append((word, (x, y), vertical))


        def get_letter_at_pos(pos):
            return board[pos1 + pos][pos2] # modyfikacja

        def no_letter_to_left(pos):
            if (
                has_room_to_left(pos)
                and board[pos1 + pos - 1][pos2]
            ): # modyfikacja
                return False
            return True

        def no_letter_to_right(pos):
            if (
                has_room_to_right(pos)
                and board[pos1 + pos + 1][pos2]
            ):# modyfikacja
                return False
            return True

        def has_room_to_left(pos):
            if pos1 + pos - 1 < 0: # modyfikacja
                return False
            return True

        def has_room_to_right(pos):
            if pos1 + pos + 1 >= 15: # modyfikacja
                return False
            return True

        # --------

        def compute_cross_sets(board):
            """
            Autorska implementacja pomysł na generację zestawu liter pozycji tzw. cross set
            "A Faster Scrabble Move Generation Algorithm"
            SOFTWARE—PRACTICE AND EXPERIENCE, VOL. 24(2), 219–232 (FEBRUARY 1994)
            Pomysł ze strony 6, przedostatni akapit
            :param board: Plansza
            :return: Zestaw skrośny do planszy
            """
            grid = [[[] for _ in range(15)] for _ in range(15)]
            for x in range(14, -1, -1):
                walking = False
                node = self.root
                position = -1
                for y in range(14, -2, -1):
                    if y != -1 and board[x][y] and not walking:
                        if board[x][y] in node.edges:
                            node = node.edges[board[x][y]]
                        else:
                            node = Node()
                        walking = True
                        if y + 1 < 15: position = y + 1
                    elif y != -1 and board[x][y]:
                        if board[x][y] in node.edges:
                            node = node.edges[board[x][y]]
                        else:
                            node = Node()
                    elif ( y == -1 or not board[x][y] ) and walking:
                        if y != -1:
                            if node.set and grid[x][y]:
                                grid[x][y] = list(set(grid[x][y]) & set(node.set))
                                if not grid[x][y]:
                                    grid[x][y] = ['x']
                            elif node.set:
                                grid[x][y] = node.set
                            else:
                                grid[x][y] = ['x']
                        if position != -1 and "|" in node.edges:
                            node = node.edges["|"]
                            if not grid[x][position] and node.set:
                                grid[x][position] = node.set
                            elif node.set:
                                word = ""
                                position_flag = False
                                for _y in range(y + 1, 15):
                                    if board[x][_y]:
                                        word = word + board[x][_y]
                                    elif not position_flag:
                                        word = word + '|'
                                        position_flag = True
                                    else:
                                        break
                                set_check = []
                                for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                                    replace_word = word.replace('|', letter)
                                    if self.is_word(replace_word):
                                        set_check.append(letter)
                                if set_check:
                                    grid[x][position] = set_check
                                else:
                                    grid[x][position] = ['x']
                            else:
                                grid[x][position] = ['x']
                        else:
                            grid[x][position] = ['x']
                        walking = False
                        position = -1
                        node = self.root
            return grid

        vertical = False
        interest = get_interesting_positions_horizontally(board)
        crosschecks = compute_cross_sets(board)
        if not interest: # plansza jest pusta
            interest.append((7, 7),) # dodaj pozycję środka planszy

        for x, y in interest:
            pos1 = x
            pos2 = y
            gen(0, "", rack, self.root)

        vertical = True
        board = [list(row) for row in zip(*board)]
        crosschecks = compute_cross_sets(board)
        interest = get_interesting_positions_horizontally(board)
        crosschecks = compute_cross_sets(board)

        for x, y in interest:
            pos1 = x
            pos2 = y
            gen(0, "", rack, self.root)

        return results

    def is_word(self, word):
        """
        Funkcja sprawdzająca, czy słowo znajduje się w słowniku
        :param word: Słowo do sprawdzenia
        :return: Prawda lub fałsz w zależności od obecności słowa w słowniku
        """
        current = self.root
        last = word[:1].upper()
        word = word[1:]

        reversed_word = ''.join(reversed(word.upper()))
        for char in reversed_word:
            if char not in current.edges:
                return False
            current = current.edges[char]
        if last in current.set:
            return True
        return False

    @staticmethod
    def calculate_play_score(board, rack, word, position, vertical):
        start_rack = rack
        # Funkcja zwracajaca wartosc podanej litery

        x, y = position
        score = 0
        multiplier = 1
        word_copy = word
        additional_score = 0
        for letter in word:
            value = get_letter_value(letter)
            if not board[x][y]:
                if (rack.count(letter) >= word_copy.count(
                        letter) or  # tyle samo lub więcej liter na stojaku niz w slowie
                        get_premium_letter_value(x, y) != 1 and rack.count(
                            letter) != 0):  # mniej liter na stojaku niz w slowie, ale nie zero i jest to pole premiowane
                    rack = rack.replace(letter, '', 1)
                    word_copy = word_copy.replace(letter, '', 1)
                else:  # mniej liter na stojaku niz w slowie oraz (pole niepremiowane lub brak liter w stojaku)
                    rack = rack.replace(' ', '', 1)
                    word_copy = word_copy.replace(letter, '', 1)
                    value = 0

                value = value * get_premium_letter_value(x, y)
                multiplier = multiplier * get_premium_word_value(x, y)

                def calculate_additional_score(x, y, dx, dy, board):
                    additional_score = 0
                    _x, _y = x + dx, y + dy
                    while 0 <= _x < 15 and 0 <= _y < 15:
                        if not board[_x][_y]:
                            break
                        additional_score += get_letter_value(board[_x][_y])
                        _x, _y = _x + dx, _y + dy
                    return additional_score

                temp_score = 0
                if vertical:
                    temp_score += calculate_additional_score(x, y, -1, 0, board)
                    temp_score += calculate_additional_score(x, y, 1, 0, board)
                else:
                    temp_score += calculate_additional_score(x, y, 0, -1, board)
                    temp_score += calculate_additional_score(x, y, 0, 1, board)
                if temp_score:
                    temp_score += value
                    temp_score *= get_premium_word_value(x, y)

                additional_score += temp_score
            score = score + value
            if vertical:
                y = y + 1
            else:
                x = x + 1
        score = score * multiplier
        score += additional_score
        if not rack and len(start_rack) == 7:
            score = score + 50
        if start_rack == rack:
            return -1000, rack
        return score, rack

    def save_to_file(self, filename):
        """
        Zapisuje obiekt WordFinderGraph do pliku.
        :param filename: ścieżka do pliku, w którym obiekt zostanie zapisany
        """
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_from_file(filename):
        """
        Odczytuje obiekt WordFinderGraph z pliku.
        :param filename: ścieżka do pliku, z którego obiekt zostanie odczytany
        :return: załadowany obiekt WordFinderGraph
        """
        with open(filename, 'rb') as file:
            return pickle.load(file)

scrabble = Scrabble.load_from_file("data/gaddag/scrabble.pkl")
size = 0