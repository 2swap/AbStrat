from steadystatec4 import check_winner
import unittest
boardheight = 6
boardwidth = 7
class TestCheckWinner(unittest.TestCase):
    def test_horizontal_win(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        player = 1
        print("a")
        for x in range(boardwidth):
            for y in range(boardheight):
                self.assertTrue(check_winner(board, player, (y,x)) == ((x == y) and x>=3))

    def test_vertical_win(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ]
        player = 1
        for x in range(boardwidth):
            for y in range(boardheight):
                self.assertTrue(check_winner(board, player, (y,x)) == ((y,x)==(2,3)))

    def test_diagonal_win(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0]
        ]
        player = 1
        for x in range(boardwidth):
            for y in range(boardheight):
                self.assertTrue(check_winner(board, player, (y,x)) == ((x==y) and x>=2))

    def test_no_win(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0]
        ]
        player = 1
        for x in range(boardwidth):
            for y in range(boardheight):
                self.assertFalse(check_winner(board, player, (y,x)) == (y>=2 and y+x==6))

