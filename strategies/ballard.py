from algorithms.scrabble import Scrabble

"""
https://cdn.aaai.org/Symposia/Fall/1993/FS-93-02/FS93-02-011.pdf
TABLE1. Weightsfor RackEvaluation Heuristic1 and Heuristic2.
"""
heuristic1 = {
    "A": 0.5,
    "B": -3.5,
    "C": -0.5,
    "D": -1,
    "E": 4,
    "F": -3,
    "G": -3.5,
    "H": 0.5,
    "I": -1.5,
    "J": -2.5,
    "K": -1.5,
    "L": -1.5,
    "M": -0.5,
    "N": 0,
    "O": -2.5,
    "P": -1.5,
    "Q": -11.5,
    "R": 1,
    "S": 7.5,
    "T": -1,
    "U": -4.5,
    "V": -6.5,
    "W": -4,
    "X": 3.5,
    "Y": -2.5,
    "Z": 3,
    " ": 24.5,
}

def ballard(player, board, words_and_positions):
    best_play = ""
    max_score = 0
    max_heuristic_score = 0
    max_rack = ""
    for word, position, direction in words_and_positions:
        score, rack = Scrabble.calculate_play_score(board, player.rack.get(), word, position, direction)
        heuristic_calculated_score = score
        for letter in rack:
            heuristic_calculated_score += heuristic1[letter]
        if heuristic_calculated_score > max_heuristic_score:
            max_score = score
            max_heuristic_score = heuristic_calculated_score
            max_rack = rack
            best_play = (word, position, direction)
    return best_play, max_score, max_rack