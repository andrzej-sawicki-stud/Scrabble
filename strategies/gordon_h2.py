from algorithms.scrabble import Scrabble

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

def gordon_h2(player, board, words_and_positions, bag, opponent):
    best_play = ""
    max_score = 0
    max_heuristic_score = 0
    max_rack = ""
    for word, position, direction in words_and_positions:
        score, rack = Scrabble.calculate_play_score(board, player.rack.get(), word, position, direction)
        heuristic_calculated_score = score
        letters_used = []
        for letter in rack:
            if letter in letters_used:
                heuristic_calculated_score += second[letter]
            else:
                heuristic_calculated_score += first[letter]
                letters_used.append(letter)
        if heuristic_calculated_score > max_heuristic_score:
            max_score = score
            max_heuristic_score = heuristic_calculated_score
            max_rack = rack
            best_play = (word, position, direction)
    return best_play, max_score, max_rack