import unittest
from chess import *

class TestChess(unittest.TestCase):
    def testPieces(self):
        board = Board()
        self.assertEqual(board.squares[1][5].piece.color, "white")
        self.assertEqual(board.getSquare(4,4).getPiece(), None)
        return
    def testValidMoves(self):
        game = Game()
        board = game.getCurrentBoard()
        self.assertNotEquals((i for i in board.getSquare(1,0).getPiece().getValidMoves() if i.getX == 0),None)
        for i in board.getAllValidMoves():
            print(i.getPieceMoved().__class__.__name__+", "+str(i.getFromSquare().getCoordinates())+"-"+str(i.getToSquare().getCoordinates()))

if __name__ == '__main__':
    unittest.main()