from algorithms.scrabble import Scrabble
import copy
from strategies.greedy import greedy
from algorithms.scrabble import scrabble, size

"""
https://cdn.aaai.org/Symposia/Fall/1993/FS-93-02/FS93-02-011.pdf
TABLE1. Weightsfor RackEvaluation Heuristic1 and Heuristic2.
"""
first = {
    "A": 1,
    "B": -3.5,
    "C": -0.5,
    "D": 0,
    "E": 4,
    "F": -2,
    "G": -2,
    "H": 0.5,
    "I": -0.5,
    "J": -3,
    "K": -2.5,
    "L": -1,
    "M": -2,
    "N": 0.5,
    "O": -1.5,
    "P": -1.5,
    "Q": -11.5,
    "R": 1.5,
    "S": 7.5,
    "T": 0,
    "U": -3,
    "V": -5.5,
    "W": -4,
    "X": 3.5,
    "Y": -2,
    "Z": 2,
    " ": 24.5,
}

"""
https://cdn.aaai.org/Symposia/Fall/1993/FS-93-02/FS93-02-011.pdf
TABLE1. Weightsfor RackEvaluation Heuristic1 and Heuristic2.
"""
second = {
    "A": -3,
    "B": -3,
    "C": -3.5,
    "D": -2.5,
    "E": -2.5,
    "F": -2,
    "G": -2.5,
    "H": -3.5,
    "I": -4,
    "L": -2,
    "M": -2,
    "N": -2.5,
    "O": -3.5,
    "P": -2.5,
    "R": -3.5,
    "S": -4,
    "T": -2.5,
    "U": -3,
    "V": -3.5,
    "W": -4.5,
    "Y": -4.5,
    " ": -15,
}

"""
https://cdn.aaai.org/Symposia/Fall/1993/FS-93-02/FS93-02-011.pdf
TABLE3. Vowel-Consonant Mix Evaluation in
RackEvaluation Heuristic3.
"""
consonants_vowels = [
    [0, 0, -1, -2, -3, -4, -5],
    [-1, 1, 1, 1, 0, -1, -2],
    [-2, 0, 2, 2, 1],
    [-3, -1, 1, 3],
    [-4, 2, 0],
    [-5, -3],
    [-6],
]

class MinimaxNode:
    def __init__(self, play=None, value=-10000):
        self.play = play
        self.value = value
        self.leaves = []



def minimax(player, opponent, board, words_and_positions, node, turn=0):
    print(minimax.size)
    if words_and_positions:
        for word, position, direction in words_and_positions:
            score, rack = Scrabble.calculate_play_score(board.get(), player.rack.get(), word, position, direction)
            if score != -1000:
                play = word, position, direction

                p = copy.deepcopy(player)
                o = copy.deepcopy(opponent)
                if turn % 2:
                    p.score += score
                    p.rack.letters = rack
                else:
                    o.score += score
                    o.rack.letters = rack

                minimax.size += 1

                if not rack:
                    p.score = p.score - p.rack.value()
                    o.score = o.score - o.rack.value()
                    if p.rack.empty():
                        p.score = p.score + o.rack.value()
                    elif o.rack.empty():
                        o.score = o.score + p.rack.value()
                    node.leaves.append(MinimaxNode(play, p.score - o.score))
                else:
                    b_copy = copy.deepcopy(board)
                    b_copy.put_word(*play)
                    n_node = MinimaxNode(play)
                    node.leaves.append(n_node)
                    if turn % 2:
                        wap = scrabble.find_all_moves(b_copy.get(), o.rack.get())
                    else:
                        wap = scrabble.find_all_moves(b_copy.get(), p.rack.get())
                    minimax(p, o, b_copy, wap, n_node, turn+1)
    else:
        minimax.size += 1

        if turn % 2:
            player.cant_move = True
        else:
            opponent.cant_move = True
        if player.cant_move and opponent.cant_move:
            player.score = player.score - player.rack.value()
            opponent.score = opponent.score - opponent.rack.value()
            if player.rack.empty():
                player.score = player.score + opponent.rack.value()
            elif opponent.rack.empty():
                opponent.score = opponent.score + player.rack.value()
            node.leaves.append(MinimaxNode(None, player.score - opponent.score))
        else:
            n_node = MinimaxNode()
            node.leaves.append(n_node)
            if turn % 2:
                wap = scrabble.find_all_moves(board.get(), opponent.rack.get())
            else:
                wap = scrabble.find_all_moves(board.get(), player.rack.get())
            minimax(player, opponent, board, wap, n_node, turn + 1)
    pass

def walk_minimax(node, turn=0):
    for leaf in node.leaves:
        walk_minimax(leaf, turn+1)
    if node.leaves:
        if turn % 2:
            val = -10000
            for leaf in node.leaves:
                if leaf.value > val:
                    val = leaf.value
                    if not turn:
                        node.play = leaf.play
        else:
            val = 10000
            for leaf in node.leaves:
                if leaf.value < val:
                    val = leaf.value
                    if not turn:
                        node.play = leaf.play




def simulate(player_d, board, opponent, play, score, rack, bag):
    player_d.rack.letters = rack
    player_d.score = player_d.score + score
    board.put_word(*play)
    opponent.strategy = greedy

    player1, player2 = opponent, player_d
    player = player2
    while (not (player.rack.empty()) and
           not (player1.cant_move and player2.cant_move)):
        if player == player1:
            player = player2
        else:
            player = player1

        words_and_positions = scrabble.find_all_moves(board.get(), player.rack.get())
        if player == player2:
            opponent = player1
        else:
            opponent = player2
        play, score, player.rack.letters = player.strategy(player, board.get(), words_and_positions, bag, opponent)
        if not words_and_positions or not play:
            player.cant_move = True
            continue
        player.cant_move = False
        board.put_word(*play)
        player.score = player.score + score

    player1.score = player1.score - player1.rack.value()
    player2.score = player2.score - player2.rack.value()
    if player1.rack.empty():
        player1.score = player1.score + player2.rack.value()
    elif player2.rack.empty():
        player2.score = player2.score + player1.rack.value()
    return player1.score - player2.score

def asawicki_h4(player, board, words_and_positions, bag, opponent):
    best_play = ""
    max_score = 0
    max_heuristic_score = 0
    max_rack = ""
    if bag.empty():
        #create minimax tree
        root = MinimaxNode()
        minimax.size = 0
        minimax(copy.deepcopy(player), copy.deepcopy(opponent), copy.deepcopy(board), words_and_positions, root)
        walk_minimax(root)
        for word, position, direction in words_and_positions:
            if (word, position, direction) == root.play:
                score, rack = Scrabble.calculate_play_score(board.get(), player.rack.get(), word, position, direction)
                max_score = score
                max_rack = rack
                best_play = (word, position, direction)
        print("dupa")
    else:
        for word, position, direction in words_and_positions:
            score, rack = Scrabble.calculate_play_score(board.get(), player.rack.get(), word, position, direction)
            if score == -1000:
                continue
            heuristic_calculated_score = score
            letters_used = []
            for letter in rack:
                if letter in letters_used:
                    heuristic_calculated_score += second[letter]
                else:
                    heuristic_calculated_score += first[letter]
                    letters_used.append(letter)
            consonants, vowels = 0, 0
            for letter in rack:
                if letter in "AEIOUY":
                    vowels += 1
                elif letter in "BCDFGHJKLMNPQRSTVWXZ":
                    consonants += 1
            heuristic_calculated_score += consonants_vowels[vowels][consonants]
            if heuristic_calculated_score > max_heuristic_score:
                max_score = score
                max_heuristic_score = heuristic_calculated_score
                max_rack = rack
                best_play = (word, position, direction)
    return best_play, max_score, max_rack