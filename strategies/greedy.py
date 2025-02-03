from algorithms.scrabble import Scrabble

def greedy(player, board, words_and_positions, bag, opponent):
    best_play = ""
    max_score = 0
    max_rack = ""
    for word, position, direction in words_and_positions:
        score, rack = Scrabble.calculate_play_score(board.get(), player.rack.get(), word, position, direction)
        if score > max_score:
            max_score = score
            max_rack = rack
            best_play = (word, position, direction)
    return best_play, max_score, max_rack