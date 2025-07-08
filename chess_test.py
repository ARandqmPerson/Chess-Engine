import unittest
from chess import *

class TestBoard(unittest.TestCase):
    def testPieces(self):
        board = Board()
        self.assertEqual(board.squares[0][1].piece.type, "R")
        self.assertEqual(board.squares[1][5].piece.color, "white")
        return

if __name__ == '__main__':
    unittest.main()