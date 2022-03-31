from enum import Flag
from hashlib import new
from itertools import count
from multiprocessing.dummy import current_process
from re import T
from unittest import result
from django.test import TestCase
from typing import List

# Create your tests here.


class Solution:

    def solveSudoku(self, board: List[List[str]]) -> None:
        def solve(i, j, hui=None):
            if hui and hui > 9:
                if log == []:
                    return False
                logpop = log.pop()
                board[logpop[0]][logpop[1]] = '.'
                used_rows[logpop[0]].remove(logpop[2])
                used_cols[logpop[1]].remove(logpop[2])
                used_grid[int(logpop[0]/3)][int(logpop[1]/3)].remove(logpop[2])
                solve(logpop[0], logpop[1], logpop[2])
            if j >= 9:
                solve(i+1, 0)
            if i >= 9:
                result.append(board)
                logpop = log.pop()
                board[logpop[0]][logpop[1]] = '.'
                used_rows[logpop[0]].remove(logpop[2])
                used_cols[logpop[1]].remove(logpop[2])
                used_grid[int(logpop[0]/3)][int(logpop[1]/3)].remove(logpop[2])
                solve(logpop[0], logpop[1], logpop[2])
            if board[i][j] != '.':
                solve(i, j+1)
            else:
                for k in range(1, 10):
                    if hui and k <= hui:
                        continue
                    if k not in used_rows[i] and k not in used_cols[j] and k not in used_grid[int(i/3)][int(j/3)]:
                        log.append([i, j, k])
                        used_rows[i].append(k)
                        used_cols[j].append(k)
                        used_grid[int(i/3)][int(j/3)].append(k)
                        board[i][j] = k
                        solve(i, j+1)
                logpop = log.pop()
                board[logpop[0]][logpop[1]] = '.'
                used_rows[logpop[0]].remove(logpop[2])
                used_cols[logpop[1]].remove(logpop[2])
                used_grid[int(logpop[0]/3)][int(logpop[1]/3)
                                            ]                         .remove(logpop[2])
                solve(logpop[0], logpop[1], logpop[2])

        result = []
        log = []
        used_rows = [[] for i in range(9)]
        used_cols = [[] for i in range(9)]
        used_grid = [[[]
                      for i in range(3)]for i in range(3)]
        for i in range(9):
            for j in range(9):
                try:
                    num = int(board[i][j])
                    used_rows[i].append(num)
                    used_cols[j].append(num)
                    used_grid[int(i/3)][int(j/3)].append(num)
                except:
                    pass
        for i in range(9):
            solve(0, i)

        # print(dp)
solution = Solution()

rs = solution.solveSudoku([["5", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."], [".", "9", "8", ".", ".", ".", ".", "6", "."], ["8", ".", ".", ".", "6", ".", ".", ".", "3"], [
                          "4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"], [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"], [".", ".", ".", ".", "8", ".", ".", "7", "9"]])
print(rs)
