#!/usr/bin/env python

import random as r
import numpy as np
import tkinter as tk

from graphics import *
from graphics_board import graphics_board

# version 2.2
# author vsoltan

""""framework for a basic tic tac toe game"""


class tic_tac_game:

    def __init__(self, boardSize=3):
        """
        :rtype: object
        :arg: size of the desired board, number
              of tokens in a row required for a win

        creates a board with passed specifications, default 3 x 3
        assigns player order and their associated tokens

        """
        self.size = boardSize

        self.board = np.empty(shape=(self.size, self.size), dtype=str)

        self.visual_board = graphics_board(self.size)

        # randomly selects the first player, player0 and player1
        self.curr_turn = r.choice([-1, 1])

        # token assignments: player1 -> X, player2 -> O
        self.token_dict = {-1: "X", 1: "O"}

        # self.image_dict = {-1: "tokenx.png", 1: "placeholder1.gif"}

        self.player_dict = {-1: "player1", 1: "player2"}

        self.score = {-1: 0, 1: 0}

        self.num_turns = 0

    # board functions
    def print_board(self):
        print(self.board)

    def check_rows(self):
        for i in range(0, self.size):
            consecutive_tokens = 0
            for j in range(0, self.size):
                if self.board[i][j] == self.token_dict[self.curr_turn]:
                    consecutive_tokens += 1
            if consecutive_tokens == self.size:
                return True
        return False

    def check_columns(self):
        for i in range(0, self.size):
            consecutive_tokens = 0
            for j in range(0, self.size):
                if self.board[j][i] == self.token_dict[self.curr_turn]:
                    consecutive_tokens += 1
            if consecutive_tokens == self.size:
                return True
        return False

    def check_diagonals(self):
        diag = np.diag(self.board)
        other_diag = np.diag(np.fliplr(self.board))

        consecutive_tokens = 1
        """initialized to 1 due to comparison-based iteration 
                ex: a = b = c -> comparing a, b, c -> (a,b) and (b,c)
                    2 comparisons for 3 consecutive tokens"""

        for i in range(0, len(diag) - 1):
            if diag[i] == diag[i + 1]:
                consecutive_tokens += 1
            if consecutive_tokens == self.size:
                return True
        else:
            consecutive_tokens = 1
        for i in range(0, len(other_diag) - 1):
            if other_diag[i] == other_diag[i + 1]:
                consecutive_tokens += 1
            if consecutive_tokens == self.size:
                return True
        return False

    def game_over(self):
        """checks whether the game is complete, win or draw"""

        # not possible to lose without taking at least 5 turns (3 x 3), 7 (4 x 4) etc
        if self.num_turns < 2 * self.size - 1: return False

        if self.check_columns() is True: return True

        if self.check_rows() is True: return True

        if self.check_diagonals() is True: return True

        return False

    def result(self, is_over):
        # if board is full but game is not over, result is a draw
        if self.num_turns == self.size ** 2 and not is_over:
            print("game is a draw!")
        else:
            print(self.player_dict[-1 * self.curr_turn] + " wins!")
            self.score[-1 * self.curr_turn] += 1

    def multiplayer(self):
        is_over = False

        while not is_over and self.num_turns != self.size ** 2:
            token = self.token_dict[self.curr_turn]

            # user input validation: can't select the same space twice
            while True:

                print(self.player_dict[self.curr_turn] + " Make your move!")
                click_point = self.visual_board.win.getMouse()
                lims = self.visual_board.limits

                move_col = self.visual_board.from_point_to_index(lims, click_point.getX())

                move_row = self.visual_board.from_point_to_index(lims, click_point.getY())

                # move_row, move_col = map(int, input(self.player_dict[self.curr_turn] +
                #                                     " make your move: input row and column").split())
                # manual testing

                if self.board[move_row][move_col] == '':
                    break
                else:
                    print("index is full, choose another space")

            # updating the logical representation of the board
            self.board[move_row][move_col] = token

            # visual update
            token_player = Text(
                Point(self.visual_board.limits[move_col] - (500 / (self.size * 2)), self.visual_board.limits[move_row] -
                      (500 / (self.size * 2))), self.token_dict[self.curr_turn])

            token_player.setFill('white')
            token_player.setSize(36)

            token_player.draw(self.visual_board.win)

            # adding rendering of token to list of all drawn objects
            self.visual_board.tokens_drawn.append(token_player)

            # increase the number of tokens
            self.num_turns += 1

            is_over = self.game_over()

            # alternate users
            self.curr_turn = -1 * self.curr_turn

            # repaint board
            self.print_board()

            self.result(is_over)

    """AI based game logic"""
    def singleplayer(self):
        return 0

    def replay(self):
        # possible text inputs to continue or terminate game
        choices = ['y', 'n']

        # temp user validation (could be another character)
        while True:
            cont = input("play again (y/n)?").strip()

            # user input validation
            if cont in choices:
                break
            else:
                print("not a valid input")

        # clears the existing board and starts a new game
        if cont == 'y':
            self.visual_board.undraw_all()
            is_over = False
            self.board = np.empty(shape=(self.size, self.size), dtype=str)
            self.num_turns = 0
            # player that just lost gets first turn CHECK THIS
            self.play_game()

        else:
            self.visual_board.win.close()
            return

    def play_game(self):
        """game logic, alternating players choosing spaces on the board to fill with their respective tokens"""

        # draws option menu
        self.visual_board.draw_menu_single_or_multiplayer()

        # draws game board
        self.visual_board.draw_game_board()

        # determines game mode
        if self.visual_board.game_mode is 0:
            self.singleplayer()
        else:
            self.multiplayer()

        self.replay()


if __name__ == "__main__":
    game = tic_tac_game()
