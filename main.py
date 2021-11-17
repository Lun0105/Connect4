# -*- coding: UTF-8 -*-
import tkinter as tk
from numpy import random
import time

class Connect_Four:
    def __init__(self):
        self.board = [["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "], ]
        self.value = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
                      10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
                      20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0,
                      30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0,
                      40: 0, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0,
                      50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: 0,
                      60: 0, 61: 0, 62: 0, 63: 0, 64: 0, 65: 0
                      }
        self.row = ["a", "b", "c", "d", "e", "f"]
        self.steps = 0
        self.chess = None

    def refresh(self):
        global warns, ans, num
        self.steps = 0
        self.board = [["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  "], ]
        self.value = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
                      10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
                      20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0,
                      30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0,
                      40: 0, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0,
                      50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: 0,
                      60: 0, 61: 0, 62: 0, 63: 0, 64: 0, 65: 0
                      }
        if ans.get() == "0" and num.get() == "1":
            n = random.randint(1, 6)
            self.board[n][0] = "○"
            self.steps += 1
        self.input_window()
        warns.set(" ")

        opp = "●"
        dot_point = 6
        blank_point = 2
        two_dot_point = 20
        for x in range(0, 7):
            for y in range(0, 6):

                hor = 0
                point = 0
                n = 0
                for i in range(x + 1, x + 4):
                    if i >= 7:
                        break
                    else:
                        if self.board[i][y] != opp:
                            point += 1
                            if self.board[i][y] == "  ":
                                hor += blank_point
                            else:
                                n += 1
                                hor += dot_point
                                if n == 2:
                                    hor += two_dot_point
                        else:
                            break
                for i in range(x - 1, x - 4, -1):
                    if i < 0:
                        break
                    else:
                        if self.board[i][y] != opp:
                            point += 1
                            if self.board[i][y] == "  ":
                                hor += blank_point
                            else:
                                n += 1
                                hor += dot_point
                                if n == 2:
                                    hor += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10 * x + y] += hor

                strai = 0
                point = 0
                n = 0
                for i in range(y + 1, y + 4):
                    if i >= 6:
                        break
                    else:
                        if self.board[x][i] != opp:
                            point += 1
                            if self.board[x][i] == "  ":
                                strai += blank_point
                            else:
                                strai += dot_point
                                n += 1
                                if n == 2:
                                    strai += two_dot_point
                        else:
                            break
                for i in range(y - 1, y - 4, -1):
                    if i < 0:
                        break
                    else:
                        if self.board[x][i] != opp:
                            point += 1
                            if self.board[x][i] == "  ":
                                strai += blank_point
                            else:
                                strai += dot_point
                                n += 1
                                if n == 2:
                                    strai += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10 * x + y] += strai

                ri_decline = 0
                point = 0
                n = 0
                for i in range(10 * x + y + 11, 10 * x + y + 44, 11):
                    if i % 10 > 5 or i // 10 > 6 or i >= 66:
                        break
                    else:
                        if self.board[i // 10][i % 10] != opp:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                ri_decline += blank_point
                            else:
                                ri_decline += dot_point
                                n += 1
                                if n == 2:
                                    ri_decline += two_dot_point
                        else:
                            break
                for i in range(10 * x + y - 11, 10 * x + y - 44, -11):
                    if i % 10 > 5 or i // 10 > 6 or i < 0:
                        break
                    else:
                        if self.board[i // 10][i % 10] != opp:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                ri_decline += blank_point
                            else:
                                ri_decline += dot_point
                                n += 1
                                if n == 2:
                                    ri_decline += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10 * x + y] += ri_decline

                lef_decline = 0
                point = 0
                n = 0
                for i in range(10 * x + y + 9, 10 * x + y + 36, 9):
                    if i % 10 > 5 or i // 10 > 6 or i >= 66:
                        break
                    else:
                        if self.board[i // 10][i % 10] != opp:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                lef_decline += blank_point
                            else:
                                lef_decline += dot_point
                                n += 1
                                if n == 2:
                                    lef_decline += two_dot_point
                        else:
                            break
                for i in range(10 * x + y - 9, 10 * x + y - 36, -9):
                    if i % 10 > 5 or i // 10 > 6 or i < 0:
                        break
                    else:
                        if self.board[i // 10][i % 10] != opp:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                lef_decline += blank_point
                            else:
                                lef_decline += dot_point
                                n += 1
                                if n == 2:
                                    lef_decline += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10 * x + y] += lef_decline
        #print("init")
        #for xi in range(0, 7):
        #    for yi in range(0, 6):
        #        if self.board[xi][yi] == "  ":
        #            print(self.value[xi * 10 + yi], " ", end='')
        #        else:
        #            print("-1 ", end='')
        #    print()
    def check(self, checking_board=None):
        if checking_board == None:
            checking_board = self.board
        for x in range(0, 7):
            for y in range(0, 3):
                if checking_board[x][y] != "  ":
                    if checking_board[x][y:y + 4] == ["○", "○", "○", "○"]:
                        return 1
                    elif checking_board[x][y:y + 4] == ["●", "●", "●", "●"]:
                        return 1
        for x in range(0, 4):
            for y in range(0, 6):
                if checking_board[x][y] != "  ":
                    test = []
                    for i in range(4):
                        test.append(checking_board[x + i][y])
                    if test == ["○", "○", "○", "○"]:
                        return 1
                    elif test == ["●", "●", "●", "●"]:
                        return 1
        for x in range(0, 4):
            for y in range(0, 3):
                if checking_board[x][y] != "  ":
                    test = []
                    for i in range(4):
                        test.append(checking_board[x + i][y + i])
                    if test == ["○", "○", "○", "○"]:
                        return 1
                    elif test == ["●", "●", "●", "●"]:
                        return 1
        for x in range(0, 4):
            for y in range(5, 2, -1):
                if checking_board[x][y] != "  ":
                    test = []
                    for i in range(4):
                        test.append(checking_board[x + i][y - i])
                    if test == ["○", "○", "○", "○"]:
                        return 1
                    elif test == ["●", "●", "●", "●"]:
                        return 1
        return 0

    def col_computer(self, n):
        global warns
        warns.set(" ")
        if self.steps % 2 == 0:
            self.chess = "○"
        else:
            self.chess = "●"
        for i in range(0, 6):
            if self.board[n][i] == "  ":
                self.board[n][i] = self.chess
                break
        self.steps += 1

    def simulate(self, n, black_or_white):
        clone = []
        for x in range(0, 7):
            line = []
            for y in range(0, 6):
                line.append(self.board[x][y])
            clone.append(line)
        for i in range(0, 6):
            if clone[n][i] == "  ":
                clone[n][i] = black_or_white
                break
        if self.check(clone):
            return 1
        else:
            return 0

    def computer_gote(self):
        if ans.get() == "0":
            com = "○"
            opp = "●"
        else:
            opp = "○"
            com = "●"
        for x in range(0,7):
            for y in range(0,6):
                self.value[10*x+y] = 0

        dot_point = 6
        blank_point = 2
        two_dot_point = 20
        for x in range(0,7):
            for y in range(0,6):

                hor = 0
                point = 0
                n = 0
                for i in range(x + 1, x + 4):
                    if i >= 7:
                        break
                    else:
                        if self.board[i][y] != com:
                            point += 1
                            if self.board[i][y] == "  ":
                                hor += blank_point
                            else:
                                n += 1
                                hor += dot_point
                                if n == 2:
                                    hor += two_dot_point
                        else:
                            break
                for i in range(x - 1, x - 4, -1):
                    if i < 0:
                        break
                    else:
                        if self.board[i][y] != com:
                            point += 1
                            if self.board[i][y] == "  ":
                                hor += blank_point
                            else:
                                n += 1
                                hor += dot_point
                                if n == 2:
                                    hor += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10*x+y] += hor

                strai = 0
                point = 0
                n = 0
                for i in range(y + 1, y + 4):
                    if i >= 6:
                        break
                    else:
                        if self.board[x][i] != com:
                            point += 1
                            if self.board[x][i] == "  ":
                                strai += blank_point
                            else:
                                strai += dot_point
                                n += 1
                                if n == 2:
                                    strai += two_dot_point
                        else:
                            break
                for i in range(y - 1, y - 4, -1):
                    if i < 0:
                        break
                    else:
                        if self.board[x][i] != com:
                            point += 1
                            if self.board[x][i] == "  ":
                                strai += blank_point
                            else:
                                strai += dot_point
                                n += 1
                                if n == 2:
                                    strai += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10*x+y] += strai

                ri_decline = 0
                point = 0
                n = 0
                for i in range(10 * x + y + 11, 10 * x + y + 44, 11):
                    if i % 10 > 5 or i // 10 > 6 or i >= 66:
                        break
                    else:
                        if self.board[i // 10][i % 10] != com:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                ri_decline += blank_point
                            else:
                                ri_decline += dot_point
                                n += 1
                                if n == 2:
                                    ri_decline += two_dot_point
                        else:
                            break
                for i in range(10 * x + y - 11, 10 * x + y - 44, -11):
                    if i % 10 > 5 or i // 10 > 6 or i < 0:
                        break
                    else:
                        if self.board[i // 10][i % 10] != com:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                ri_decline += blank_point
                            else:
                                ri_decline += dot_point
                                n += 1
                                if n == 2:
                                    ri_decline += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10 * x + y] += ri_decline

                lef_decline = 0
                point = 0
                n = 0
                for i in range(10 * x + y + 9, 10 * x + y + 36, 9):
                    if i % 10 > 5 or i // 10 > 6 or i >= 66:
                        break
                    else:
                        if self.board[i // 10][i % 10] != com:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                lef_decline += blank_point
                            else:
                                lef_decline += dot_point
                                n += 1
                                if n == 2:
                                    lef_decline += two_dot_point
                        else:
                            break
                for i in range(10 * x + y - 9, 10 * x + y - 36, -9):
                    if i % 10 > 5 or i // 10 > 6 or i < 0:
                        break
                    else:
                        if self.board[i // 10][i % 10] != com:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                lef_decline += blank_point
                            else:
                                lef_decline += dot_point
                                n += 1
                                if n == 2:
                                    lef_decline += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10*x+y] += lef_decline

        for x in range(0,7):
            for y in range(0,6):

                hor = 0
                point = 0
                n = 0
                for i in range(x + 1, x + 4):
                    if i >= 7:
                        break
                    else:
                        if self.board[i][y] != opp:
                            point += 1
                            if self.board[i][y] == "  ":
                                pass
                            else:
                                hor += dot_point
                                n += 1
                                if n == 2:
                                    hor += two_dot_point
                        else:
                            break
                for i in range(x - 1, x - 4, -1):
                    if i < 0:
                        break
                    else:
                        if self.board[i][y] != opp:
                            point += 1
                            if self.board[i][y] == "  ":
                                pass
                            else:
                                hor += dot_point
                                n += 1
                                if n == 2:
                                    hor += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10*x+y] += hor

                strai = 0
                point = 0
                n = 0
                for i in range(y + 1, y + 4):
                    if i >= 6:
                        break
                    else:
                        if self.board[x][i] != opp:
                            point += 1
                            if self.board[x][i] == "  ":
                                pass
                            else:
                                strai += dot_point
                                n += 1
                                if n == 2:
                                    strai += two_dot_point
                        else:
                            break
                for i in range(y - 1, y - 4, -1):
                    if i < 0:
                        break
                    else:
                        if self.board[x][i] != opp:
                            point += 1
                            if self.board[x][i] == "  ":
                                pass
                            else:
                                strai += dot_point
                                n += 1
                                if n == 2:
                                    strai += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10*x+y] += strai

                ri_decline = 0
                point = 0
                n = 0
                for i in range(10 * x + y + 11, 10 * x + y + 44, 11):
                    if i % 10 > 5 or i // 10 > 6 or i >= 66:
                        break
                    else:
                        if self.board[i // 10][i % 10] != opp:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                pass
                            else:
                                ri_decline += dot_point
                                n += 1
                                if n == 2:
                                    ri_decline += two_dot_point
                        else:
                            break
                for i in range(10 * x + y - 11, 10 * x + y - 44, -11):
                    if i % 10 > 5 or i // 10 > 6 or i < 0:
                        break
                    else:
                        if self.board[i // 10][i % 10] != opp:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                pass
                            else:
                                ri_decline += dot_point
                                n += 1
                                if n == 2:
                                    ri_decline += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10 * x + y] += ri_decline

                lef_decline = 0
                point = 0
                n = 0
                for i in range(10 * x + y + 9, 10 * x + y + 36, 9):
                    if i % 10 > 5 or i // 10 > 6 or i >= 66:
                        break
                    else:
                        if self.board[i // 10][i % 10] != opp:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                pass
                            else:
                                lef_decline += dot_point
                                n += 1
                                if n == 2:
                                    lef_decline += two_dot_point
                        else:
                            break
                for i in range(10 * x + y - 9, 10 * x + y - 36, -9):
                    if i % 10 > 5 or i // 10 > 6 or i < 0:
                        break
                    else:
                        if self.board[i // 10][i % 10] != opp:
                            point += 1
                            if self.board[i // 10][i % 10] == "  ":
                                pass
                            else:
                                lef_decline += dot_point
                                n += 1
                                if n == 2:
                                    lef_decline += two_dot_point
                        else:
                            break
                if point >= 3:
                    self.value[10*x+y] += lef_decline
        for x in range(0,7):
            for y in range(0,6):
                if self.value[10*x+y] == 0:
                    self.value[10*x+y] = 2

        for x in range(0, 7):
            clone = []
            for xi in range(0, 7):
                line = []
                for yi in range(0, 6):
                    line.append(self.board[xi][yi])
                clone.append(line)
            for y in range(0, 6):
                if clone[x][y] == "  " and y != 5:
                    clone[x][y + 1] = opp
                    if self.check(clone):
                        #print(x)
                        self.value[10 * x + y] = 0
                        self.value[10 * x + y] = 0
                    break

        #print("value")
        #for xi in range(0, 7):
        #    for yi in range(0, 6):
        #        if self.board[xi][yi] == "  ":
        #            print(self.value[xi * 10 + yi], " ", end='')
        #        else:
        #            print("-1 ", end='')
        #    print()

        highest_value = 0
        for x in range(0, 7):
            for y in range(0, 6):
                if self.board[x][y] == "  ":
                    if self.value[(10 * x) + y] >= highest_value:
                        highest_value = self.value[(10 * x) + y]
                        n = x
                    break
        for i in range(0, 7):
            if self.simulate(i, opp):
                n = i
        for i in range(0, 7):
            if self.simulate(i, com):
                n = i
        self.col_computer(n)


    def input_window(self):
        global row1chess, row2chess, row3chess, row4chess, row5chess, row6chess, row7chess, steps_num, warn, num, ans
        buttons.pack(side="top")
        for x in range(7):
            line = ""
            if x == 0:
                for y in range(5, -1, -1):
                    line += self.board[x][y]
                    if y != 0:
                        line += "\n\n"
                row1chess.set(line)
            elif x == 1:
                for y in range(5, -1, -1):
                    line += self.board[x][y]
                    if y != 0:
                        line += "\n\n"
                row2chess.set(line)
            elif x == 2:
                for y in range(5, -1, -1):
                    line += self.board[x][y]
                    if y != 0:
                        line += "\n\n"
                row3chess.set(line)
            elif x == 3:
                for y in range(5, -1, -1):
                    line += self.board[x][y]
                    if y != 0:
                        line += "\n\n"
                row4chess.set(line)
            elif x == 4:
                for y in range(5, -1, -1):
                    line += self.board[x][y]
                    if y != 0:
                        line += "\n\n"
                row5chess.set(line)
            elif x == 5:
                for y in range(5, -1, -1):
                    line += self.board[x][y]
                    if y != 0:
                        line += "\n\n"
                row6chess.set(line)
            elif x == 6:
                for y in range(5, -1, -1):
                    line += self.board[x][y]
                    if y != 0:
                        line += "\n\n"
                row7chess.set(line)
        steps_num.set(f"steps:{self.steps}")
        if self.check():
            if num.get() == "0":
                if self.steps % 2 == 0:
                    n = "○Succeeding"
                else:
                    n = "●Preceding"
                warn.set(f"{n} player Wins !")
            else:
                if ans.get() == "1":
                    if self.steps % 2 == 1:
                        warn.set("○Player Wins !")
                    else:
                        warn.set("You Lose !")
                else:
                    if self.steps % 2 == 1:
                        warn.set("You Lose !")
                    else:
                        warn.set("●Player Wins !")
            buttons.pack_forget()
        elif self.steps == 42:
            warn.set("Game Tied !")
            buttons.pack_forget()
        else:
            if self.steps % 2 == 0:
                n = "Preceding player"
            else:
                n = "Succeeding player"
            warn.set(f"{n} choose a column to put your chess:")

    def col1(self):
        global warns
        warns.set(" ")
        fail = True
        self.steps += 1
        if self.steps % 2:
            self.chess = "○"
        else:
            self.chess = "●"
        loops = 0
        for i in self.board[0]:
            if i == "  ":
                self.board[0][loops] = self.chess
                break
            if loops == 5:
                warns.set("You can't put a chess here. Try again!")
                fail = False
                self.steps -= 1
            loops += 1
        self.input_window()
        global num
        if num.get() == "1" and fail:
            if self.check():
                pass
            else:
                self.computer_gote()
                self.input_window()

    def col2(self):
        global warns
        warns.set(" ")
        fail = True
        self.steps += 1
        if self.steps % 2:
            self.chess = "○"
        else:
            self.chess = "●"
        loops = 0
        for i in self.board[1]:
            if i == "  ":
                self.board[1][loops] = self.chess
                break
            if loops == 5:
                warns.set("You can't put a chess here. Try again!")
                fail = False
                self.steps -= 1
            loops += 1
        self.input_window()
        global num
        if num.get() == "1" and fail:
            if self.check():
                pass
            else:
                self.computer_gote()
                self.input_window()

    def col3(self):
        global warns
        warns.set(" ")
        fail = True
        self.steps += 1
        if self.steps % 2:
            self.chess = "○"
        else:
            self.chess = "●"
        loops = 0
        for i in self.board[2]:
            if i == "  ":
                self.board[2][loops] = self.chess
                break
            if loops == 5:
                warns.set("You can't put a chess here. Try again!")
                fail = False
                self.steps -= 1
            loops += 1
        self.input_window()
        global num
        if num.get() == "1" and fail:
            if self.check():
                pass
            else:
                self.computer_gote()
                self.input_window()

    def col4(self):
        global warns
        warns.set(" ")
        fail = True
        self.steps += 1
        if self.steps % 2:
            self.chess = "○"
        else:
            self.chess = "●"
        loops = 0
        for i in self.board[3]:
            if i == "  ":
                self.board[3][loops] = self.chess
                break
            if loops == 5:
                warns.set("You can't put a chess here. Try again!")
                fail = False
                self.steps -= 1
            loops += 1
        self.input_window()
        global num
        if num.get() == "1" and fail:
            if self.check():
                pass
            else:
                self.computer_gote()
                self.input_window()

    def col5(self):
        global warns
        warns.set(" ")
        fail = True
        self.steps += 1
        if self.steps % 2:
            self.chess = "○"
        else:
            self.chess = "●"
        loops = 0
        for i in self.board[4]:
            if i == "  ":
                self.board[4][loops] = self.chess
                break
            if loops == 5:
                warns.set("You can't put a chess here. Try again!")
                fail = False
                self.steps -= 1
            loops += 1
        self.input_window()
        global num
        if num.get() == "1" and fail:
            if self.check():
                pass
            else:
                self.computer_gote()
                self.input_window()

    def col6(self):
        global warns
        warns.set(" ")
        fail = True
        self.steps += 1
        if self.steps % 2:
            self.chess = "○"
        else:
            self.chess = "●"
        loops = 0
        for i in self.board[5]:
            if i == "  ":
                self.board[5][loops] = self.chess
                break
            if loops == 5:
                warns.set("You can't put a chess here. Try again!")
                fail = False
                self.steps -= 1
            loops += 1
        self.input_window()
        global num
        if num.get() == "1" and fail:
            if self.check():
                pass
            else:
                self.computer_gote()
                self.input_window()

    def col7(self):
        global warns
        warns.set(" ")
        fail = True
        self.steps += 1
        if self.steps % 2:
            self.chess = "○"
        else:
            self.chess = "●"
        loops = 0
        for i in self.board[6]:
            if i == "  ":
                self.board[6][loops] = self.chess
                break
            if loops == 5:
                warns.set("You can't put a chess here. Try again!")
                fail = False
                self.steps -= 1
            loops += 1
        self.input_window()
        global num
        if num.get() == "1" and fail:
            if self.check():
                pass
            else:
                self.computer_gote()
                self.input_window()


player = Connect_Four()

window = tk.Tk()
window.title("Connect4")
window.geometry("750x570")
tittle_window = tk.Label(window, text="$ Connect4 $", bg=None, font=('Times', 20, 'bold italic'), width=12,
                         height=1).pack()

chose_player = tk.Frame(window)
chose_player.pack(side="top")


def selected():
    player.refresh()


num = tk.StringVar()
num.set("0")
player_num = tk.Radiobutton(chose_player, text="1 Player", variable=num, value=True, command=selected, indicatoron=0)
player_num.pack(side='left')
player_num2 = tk.Radiobutton(chose_player, text="2 Players(default)", variable=num, value=False, command=selected,
                             indicatoron=0)
player_num2.pack(side='left')


def init_decided():
    if num.get() == "1":
        player.refresh()
    else:
        warns.set("No need to choose in Player2 mode!")


ans = tk.StringVar()
ans.set("1")
ask = tk.Label(chose_player, text="Do you want to go first ? ", font=("Arial", 12), width=20, height=1).pack(
    side="left")
init = tk.Radiobutton(chose_player, text="Preceding(default)", variable=ans, value=True, command=init_decided)
init.pack(side='left')
before = tk.Radiobutton(chose_player, text="Succeeding", variable=ans, value=False, command=init_decided)
before.pack(side='left')

info = tk.Frame(window)
info.pack(side='top')
player_window = tk.Label(info, text="Preceding Player:○ Succeeding player:●",
                         bg=None, font=('Arial', 14), width=31, height=1)
player_window.pack(side='left')
steps_num = tk.StringVar()
steps_num.set("steps:0")
steps_info = tk.Label(info, textvariable=steps_num, bg=None, font=('Times', 16), width=8, height=1).pack(side='left')
refresh_button = tk.Button(info, text="New Game", width=9, height=1, command=player.refresh)
refresh_button.pack()

board = tk.Frame(window)
board.pack(side='top')
row0 = tk.Label(board, text='a\n\nb\n\nc\n\nd\n\ne\n\nf'
                , relief="raised", bg="DarkGrey", font=('time', 20), width=3, height=12).pack(side='left')

row1chess = tk.StringVar()
row1 = tk.Label(board, textvariable=row1chess, relief="raised", bg="LightGrey", font=('time', 20), width=4,
                height=12).pack(side='left')

row2chess = tk.StringVar()
row2 = tk.Label(board, textvariable=row2chess, relief="raised", bg="darkgrey", font=('time', 20), width=4,
                height=12).pack(side='left')

row3chess = tk.StringVar()
row3 = tk.Label(board, textvariable=row3chess, relief="raised", bg="LightGrey", font=('time', 20), width=4,
                height=12).pack(side='left')

row4chess = tk.StringVar()
row4 = tk.Label(board, textvariable=row4chess, relief="raised", bg="darkgrey", font=('time', 20), width=4,
                height=12).pack(side='left')

row5chess = tk.StringVar()
row5 = tk.Label(board, textvariable=row5chess, relief="raised", bg="LightGrey", font=('time', 20), width=4,
                height=12).pack(side='left')

row6chess = tk.StringVar()
row6 = tk.Label(board, textvariable=row6chess, relief="raised", bg="darkgrey", font=('time', 20), width=4,
                height=12).pack(side='left')

row7chess = tk.StringVar()
row7 = tk.Label(board, textvariable=row7chess, relief="raised", bg="LightGrey", font=('time', 20), width=4,
                height=12).pack(side='left')

label = tk.Label(window, text="     1      2      3      4      5      6      7",
                 relief="raised", bg="LightGrey", font=('Arial', 20), width=30, height=1).pack(side='top')

warns = tk.StringVar()
tip = tk.Label(window, textvariable=warns, font=('Arial', 12,), fg='red', width=50, height=1).pack(side='top')

warn = tk.StringVar()
warn.set("Preceding player choose a column to put your chess:")
tips = tk.Label(window, textvariable=warn, font=('Arial', 16), width=50, height=1).pack(side='top')

blank = tk.Label(window, text=" ", font=("Arial", 2), width=1, height=1).pack(side="top")

buttons = tk.Frame(window)
buttons.pack(side='top')

col1but = tk.Button(buttons, text="column1", font=('Arial', 12), width=6, height=1, command=player.col1)
col1but.pack(side='left')
blank0 = tk.Label(buttons, text=" ", width=1, height=1).pack(side="left")
col2but = tk.Button(buttons, text="column2", font=('Arial', 12), width=6, height=1, command=player.col2)
col2but.pack(side='left')
blank1 = tk.Label(buttons, text=" ", width=1, height=1).pack(side="left")
col3but = tk.Button(buttons, text="column3", font=('Arial', 12), width=6, height=1, command=player.col3)
col3but.pack(side='left')
blank2 = tk.Label(buttons, text=" ", width=1, height=1).pack(side="left")
col4but = tk.Button(buttons, text="column4", font=('Arial', 12), width=6, height=1, command=player.col4)
col4but.pack(side='left')
blank3 = tk.Label(buttons, text=" ", width=1, height=1).pack(side="left")
col5but = tk.Button(buttons, text="column5", font=('Arial', 12), width=6, height=1, command=player.col5)
col5but.pack(side='left')
blank4 = tk.Label(buttons, text=" ", width=1, height=1).pack(side="left")
col6but = tk.Button(buttons, text="column6", font=('Arial', 12), width=6, height=1, command=player.col6)
col6but.pack(side='left')
blank5 = tk.Label(buttons, text=" ", width=1, height=1).pack(side="left")
col7but = tk.Button(buttons, text="column7", font=('Arial', 12), width=6, height=1, command=player.col7)
col7but.pack(side='left')
blank6 = tk.Label(buttons, text=" ", width=1, height=1).pack(side="left")

window.mainloop()
