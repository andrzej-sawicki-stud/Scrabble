import json
from math import floor

import matplotlib.pyplot as plt
import numpy as np

with (open('data/games.json') as file):
    games = json.load(file)
    words = {}
    scores = {}
    total_count = 0
    total_time = 0
    total_score = 0
    total_bingo_score = 0
    frequency_len = [0, 0, 0, 0, 0, 0, 0]
    frequency_score = [0, 0, 0, 0, 0, 0, 0]
    word_len = [0, 0, 0, 0, 0, 0, 0, 0]
    word_score = [0, 0, 0, 0, 0, 0, 0, 0]
    word_per_game = []
    average = []
    bingo_count = []
    bingo = []
    other = []
    turn_count = []
    one_rack = {}
    two_rack = {}
    when_played = {}
    num_of_consontants, num_of_vowels = 0,0
    prev_score = 0
    consontant_vowel_count = [[0 for _ in range(7)] for _ in range(7)]
    consontant_vowel_score = [[0 for _ in range(7)] for _ in range(7)]
    for j in range(50):
        average.append(0)
        bingo.append(0)
        bingo_count.append(0)
        other.append(0)
        turn_count.append(0)
    for i in range(25000):
        game = games[str(i)]
        total_time += game["time"]
        moves = game["moves"]
        turn = -1
        prev_score = -1
        for move in moves:

            turn += 1
            turn_count[turn] += 1
            rack, end_rack, play, score = move
            if prev_score != -1 and turn == 10:
                consontant_vowel_score[num_of_vowels][num_of_consontants] += score
                consontant_vowel_count[num_of_vowels][num_of_consontants] += 1
            num_of_vowels = 0
            num_of_consontants = 0
            word, position, vertical = play
            if word not in words:
                words[word] = 1
                scores[word] = score
            else:
                words[word] += 1
                scores[word] += score
            total_count += 1
            total_score += score
            frequency_len[len(rack)-len(end_rack)-1] += 1
            frequency_score[len(rack) - len(end_rack)-1] += score
            # word_game = [0, 0, 0, 0, 0, 0, 0, 0]
            if turn % 2 == 0:
                if len(word) < 9:
                    word_len[len(word)-2] += 1
                    word_score[len(word)-2] += score
                    # word_game[len(word)-2] += score
                else:
                    word_len[7] += 1
                    word_score[7] += score
                    # word_game[7] += score
            average[turn] += score
            if len(rack)-len(end_rack) == 7:
                bingo[turn] += score
                bingo_count[turn] += 1
                total_bingo_score += score
            else:
                other[turn] += score
            for letter in " ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if letter in rack:
                    if letter not in one_rack:
                        one_rack[letter] = []
                    one_rack[letter].append(score)
                    rem_rack = rack.replace(letter, "", 1)
                    if letter in rem_rack:
                        if letter not in two_rack:
                            two_rack[letter] = []
                        two_rack[letter].append(score)
                if letter in word:
                    if letter not in when_played:
                        when_played[letter] = []
                    when_played[letter].append(score)
                elif letter == " ":
                    for l in word:
                        if l in rack:
                            rack = rack.replace(l, "", 1)
                        else:
                            if letter not in when_played:
                                when_played[letter] = []
                            when_played[letter].append(score)
                            break
            for letter in end_rack:
                if letter in "AEIOUY":
                    num_of_vowels += 1
                else:
                    num_of_consontants += 1
            prev_score = score
    for i in range(7):
        print(consontant_vowel_score[i])

    for i in range(7):
        for j in range(7):
            if consontant_vowel_count[i][j] != 0:
                consontant_vowel_score[i][j] /= consontant_vowel_count[i][j]

    for i in range(7):
        print(consontant_vowel_score[i])

    # for i in range(7):
    #     for j in range(7):
    #         if consontant_vowel_score[i][j]:
    #             consontant_vowel_score[0][i+j] += consontant_vowel_score[i][j]
    #             consontant_vowel_count[0][i + j] += consontant_vowel_count[i][j]
    #
    # for i in range(7):
    #     consontant_vowel_score[0][i] /= consontant_vowel_count[0][i]
    #
    # print(consontant_vowel_score[0])



    # print(total_bingo_score/total_score*100)
    # print("one rack")
    # for key, value in one_rack.items():
    #     if len(value):
    #         print(key, sum(value)/len(value))
    # print("two rack")
    # for key, value in two_rack.items():
    #     if len(value):
    #         print(key, sum(value) / len(value))
    # print("when played")
    # for key, value in when_played.items():
    #     if len(value):
    #         print(key, sum(value) / len(value))
    # print("Average time: ", total_time/25000)
    # for i in range(8):
    #     print(i+2, word_len[i]/total_count*100, word_score[i]/word_len[i], word_score[i]/25000)
    # for i in range(50):
    #     if bingo_count[i]:
    #         print(i+1, average[i]/turn_count[i], bingo_count[i]/turn_count[i]*100, bingo[i]/bingo_count[i], other[i]/(turn_count[i]-bingo_count[i]))
    #     elif turn_count[i]:
    #         print(i + 1, average[i] / turn_count[i], 0, 0,
    #               other[i] / turn_count[i])
    #     else:
    #         print(i + 1, 0, 0, 0,
    #               0)
    # for i in range(6, -1, -1):
    #     print(i+1, frequency_len[i]/total_count*100, frequency_score[i]/frequency_len[i])
    # sorted_words = sorted(words.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    # ten_pr = floor(len(words)/10)
    # for i in range(1, 11):
    #     num = ten_pr * i
    #     freq = 0
    #     scr = 0
    #     z = 0
    #     for pair in sorted_words:
    #         word, frequency = pair
    #         z += 1
    #         scr += scores[word]
    #         freq += frequency
    #         if z == num:
    #             break
    #     print(i, num, freq/total_count*100, scr/total_score*100)
    # for pair in sorted_words:
    #     word, frequency = pair
    #     if ("J" in word or
    #         "Q" in word or
    #         "X" in word or
    #         "Z" in word
    #     ):
    #         print(word, frequency, frequency/total_count, scores[word]/frequency)

    # positions = [[0 for _ in range(15)] for _ in range(15)]
    # for i in range(25000):
    #     game = games[str(i)]
    #     board = game["board"]
    #     for y in range(15):
    #         for x in range(15):
    #             if board[x][y]:
    #                 positions[x][y] += 1
    # for y in range(15):
    #     for x in range(15):
    #         positions[x][y] = 255 - positions[x][y] / 1000 * 255
    #
    # scores = [[0 for _ in range(15)] for _ in range(15)]
    # usage = [[0 for _ in range(15)] for _ in range(15)]
    # for i in range(25000):
    #     game = games[str(i)]
    #     moves = game["moves"]
    #     for move in moves:
    #         rack, end_rack, play, score = move
    #         word, position, vertical = play
    #         x, y = position
    #         if not vertical:
    #             for a in range(len(word)):
    #                 scores[x + a][y] += score
    #                 usage[x + a][y] += 1
    #         else:
    #             for a in range(len(word)):
    #                 scores[x][y + a] += score
    #                 usage[x][y + a] += 1
    # max = 0
    # for y in range(15):
    #     for x in range(15):
    #         if scores[x][y] > max:
    #             max = scores[x][y]
    # for y in range(15):
    #     for x in range(15):
    #         scores[x][y] = scores[x][y] / usage[x][y]
    #         scores[x][y] = 255 - scores[x][y] / max * 255
    #
    # positions_array = np.array(positions)
    # plt.figure(figsize=(15, 15))  # Rozmiar wykresu
    # plt.imshow(positions_array, cmap='gray', interpolation='nearest')  # Szachownica w odcieniach szarości
    # #plt.colorbar(label='Częstotliwość')  # Pasek kolorów z opisem
    # #plt.title("Wykorzystanie pól")
    # plt.axis('off')  # Ukrycie osi
    # plt.show()
    #
    # positions_array = np.array(scores)
    # plt.figure(figsize=(15, 15))  # Rozmiar wykresu
    # plt.imshow(positions_array, cmap='gray', interpolation='nearest')  # Szachownica w odcieniach szarości
    # #plt.colorbar(label='Średnia wartość ruchu')  # Pasek kolorów z opisem
    # #plt.title("Wartość ruchu zawierającego dane pole")
    # plt.axis('off')  # Ukrycie osi
    # plt.show()
