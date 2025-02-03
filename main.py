import time
import json

from algorithms.scrabble import scrabble
from strategies.greedy import greedy
from strategies.ballard import ballard
from strategies.gordon_h2 import gordon_h2
from strategies.gordon_h3 import gordon_h3
from strategies.asawicki_h3 import asawicki_h3
from strategies.asawicki_h4 import asawicki_h4

from structures.board import Board
from structures.bag import Bag
from structures.player import Player



if __name__ == "__main__":


    ballard_sum, greedy_sum = 0, 0
    ballard_win = 0

    for i in range(1000):
        bag = Bag()
        board = Board()
        if i % 2 == 0:
            player1, player2 = Player("1", asawicki_h4), Player("2", greedy)
        else:
            player1, player2 = Player("1", greedy), Player("2", asawicki_h4)
        player1.rack.letters, player2.rack.letters = bag.fill_rack(player1.rack.get()), bag.fill_rack(player2.rack.get())
        player = player2
        turn = 0
        start_time = time.time()
        while (not (player.rack.empty() and bag.empty()) and
               not (player1.cant_move and player2.cant_move)):
            turn = turn + 1
            if player == player1: player = player2
            else: player = player1

            rack = player.rack.letters
            words_and_positions = scrabble.find_all_moves(board.get(), player.rack.get())
            if player == player2:
                opponent = player1
            else:
                opponent = player2
            play, score, player.rack.letters = player.strategy(player, board, words_and_positions, bag, opponent)
            if not words_and_positions or not play:
                player.cant_move = True
                continue
            player.cant_move = False
            board.put_word(*play)
            player.score = player.score + score
            player.rack.letters = bag.fill_rack(player.rack.get())

        player1.score = player1.score - player1.rack.value()
        player2.score = player2.score - player2.rack.value()
        if player1.rack.empty():
            player1.score = player1.score + player2.rack.value()
        elif player2.rack.empty():
            player2.score = player2.score + player1.rack.value()

        if i % 2 == 0:
            ballard_sum += player1.score
            greedy_sum += player2.score
        else:
            ballard_sum += player2.score
            greedy_sum += player1.score
        if i % 2 == 0:
            if player2.score < player1.score:
                ballard_win += 1
        else:
            if player1.score < player2.score:
                ballard_win += 1
    print(ballard_win)
    print(ballard_sum / 1000)
    print(greedy_sum / 1000)
