import unittest
from chess import *

class TestChessBasic(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
        return super().setUp()
    def testPieceSetup(self):
        game = self.game
        board = self.board
        self.assertEqual(board.getSquare(5,1).piece.color, "white")
        self.assertEqual(board.getSquare(4,4).piece, None)
        return
    def testInitialValidMoves(self):
        game = self.game
        board = self.board
        pawn = board.getSquare(0,1).piece
        rook = board.getSquare(0,0).piece
        knight = board.getSquare(1,0).piece
        bishop = board.getSquare(2,0).piece
        queen = board.getSquare(3,0).piece
        king = board.getSquare(4,0).piece
        self.assertEqual(pawn.getValidMoveCoordinates(),[(0,2),(0,3)])
        self.assertEqual(bishop.getValidMoveCoordinates(),[])
        self.assertCountEqual(knight.getValidMoveCoordinates(),[(2,2),(0,2)])
    def testInitialThreatenedSquares(self):
        game = self.game
        board = self.board
        pawn = board.getSquare(0,1).piece
        knight = board.getSquare(1,0).piece
        bishop = board.getSquare(2,0).piece
        self.assertEqual(pawn.getThreatenedSquareCoordinates(),[(1,2)])
        self.assertCountEqual(knight.getThreatenedSquareCoordinates(),[(0,2),(2,2),(3,1)])
        self.assertCountEqual(bishop.getThreatenedSquareCoordinates(),[(1,1),(0,2),(3,1),(4,2),(5,3),(6,4),(7,5)])
    def testMove(self):
        game = self.game
        board = self.board
        game.makeMove([4,1],[4,3])
        self.assertNotEqual(board.getSquare(4,3).piece,None)
        self.assertEqual(board.getSquare(4,1).piece,None)
        self.assertEqual(game.moveNumber,1)
        self.assertEqual(game.whoseMove,"black")

class TestMultipleMoves(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
        self.game.makeMove([4,1],[4,3])
        self.game.makeMove([4,6],[4,4])
        self.game.makeMove([3,0],[7,4])
        self.game.makeMove([6,7],[5,5])
        self.game.makeMove([7,4],[5,6])
        return
    def testGameInfo(self):
        self.assertEqual(self.game.whoseMove,"black")
        self.assertEqual(self.game.moveNumber,3)
        return
    def testPieceLocations(self):
        game = self.game
        ideallyQueen = game.board.getSquare(5,6).piece
        self.assertEqual(ideallyQueen.__class__.__name__,"Queen")
        return
    def testIsKingInCheck(self):
        self.assertEqual(self.game.board.whichKingInCheck, "black")
    def testMoveListAndNotation(self):
        self.game.displayMoveList()
        self.assertEqual(self.game.moveList[0].notation, "e4")
        self.assertEqual(self.game.moveList[4].notation, "Qxf7+")

class TestMoveNotation(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
    # Will cause an error if the move notation isn't recognized
    def testAmbiguousMoveNotation(self):
        self.game.makeMoveUsingNotation("d3")
        self.game.makeMoveUsingNotation("d6")
        self.game.makeMoveUsingNotation("Nf3")
        self.game.makeMoveUsingNotation("Nf6")
        self.game.makeMoveUsingNotation("Nbd2")
        self.game.makeMoveUsingNotation("Nbd7")
        self.game.makeMoveUsingNotation("Nd4")
        self.game.makeMoveUsingNotation("Nd5")
        self.game.makeMoveUsingNotation("N2b3")
        self.game.makeMoveUsingNotation("N7b6")

class TestEnPassant(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
    # Tests whether en passant is correctly recognized as valid and played
    # and whether it's correctly recognized as invalid
    def testEnPassant(self):
        self.game.makeMoveUsingNotation("e4")
        self.game.makeMoveUsingNotation("e6")
        self.game.makeMoveUsingNotation("e5")
        self.game.makeMoveUsingNotation("d5")
        self.game.makeMoveUsingNotation("exd6")
        self.assertEqual(self.board.getSquare(3,5).piece.type,"p")
        self.assertEqual(self.board.getSquare(3,4).piece,None)

if __name__ == '__main__':
    unittest.main()