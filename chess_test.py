import unittest
from chess import *

class TestChessBasic(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.getBoard()
        return super().setUp()
    def testPieceSetup(self):
        game = self.game
        board = self.board
        self.assertEqual(board.getSquare(5,1).piece.color, "white")
        self.assertEqual(board.getSquare(4,4).getPiece(), None)
        return
    def testInitialValidMoves(self):
        game = self.game
        board = self.board
        pawn = board.getSquare(0,1).getPiece()
        rook = board.getSquare(0,0).getPiece()
        knight = board.getSquare(1,0).getPiece()
        bishop = board.getSquare(2,0).getPiece()
        queen = board.getSquare(3,0).getPiece()
        king = board.getSquare(4,0).getPiece()
        self.assertEquals(pawn.getValidMoveCoordinates(),[(0,2),(0,3)])
        self.assertEquals(bishop.getValidMoveCoordinates(),[])
        self.assertCountEqual(knight.getValidMoveCoordinates(),[(2,2),(0,2)])
    def testInitialThreatenedSquares(self):
        game = self.game
        board = self.board
        pawn = board.getSquare(0,1).getPiece()
        knight = board.getSquare(1,0).getPiece()
        bishop = board.getSquare(2,0).getPiece()
        self.assertEquals(pawn.getThreatenedSquareCoordinates(),[(1,2)])
        self.assertCountEqual(knight.getThreatenedSquareCoordinates(),[(0,2),(2,2),(3,1)])
        self.assertCountEqual(bishop.getThreatenedSquareCoordinates(),[(1,1),(0,2),(3,1),(4,2),(5,3),(6,4),(7,5)])
    def testMove(self):
        game = self.game
        board = self.board
        game.makeMove([4,1],[4,3])
        self.assertNotEquals(board.getSquare(4,3).getPiece(),None)
        self.assertEquals(board.getSquare(4,1).getPiece(),None)
        self.assertEquals(game.getMoveNumber(),1)
        self.assertEquals(game.getWhoseMove(),"black")

class TestMultipleMoves(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.getBoard()
        print(self.game.makeMove([4,1],[4,3]))
        print(self.game.makeMove([4,6],[4,4]))
        print(self.game.makeMove([3,0],[7,4]))
        print(self.game.makeMove([6,7],[5,5]))
        print(self.game.makeMove([7,4],[5,6]))
        return
    def testGameInfo(self):
        self.assertEquals(self.game.getWhoseMove(),"black")
        self.assertEquals(self.game.getMoveNumber(),3)
        return
    def testPieceLocations(self):
        game = self.game
        for piece in self.board.getAllActivePieces():
            print(piece.getColor()+" "+piece.__class__.__name__+", "+str(piece.getCoordinates()))
        ideallyQueen = game.getBoard().getSquare(5,6).getPiece()
        self.assertEquals(ideallyQueen.__class__.__name__,"Queen")
        return

if __name__ == '__main__':
    unittest.main()