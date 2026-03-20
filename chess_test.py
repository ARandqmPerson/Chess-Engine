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
        print(self.game.makeMove([4,1],[4,3]))
        print(self.game.makeMove([4,6],[4,4]))
        print(self.game.makeMove([3,0],[7,4]))
        print(self.game.makeMove([6,7],[5,5]))
        print(self.game.makeMove([7,4],[5,6]))
        return
    def testGameInfo(self):
        self.assertEqual(self.game.whoseMove,"black")
        self.assertEqual(self.game.moveNumber,3)
        return
    def testPieceLocations(self):
        game = self.game
        # # For testing:
        # for piece in self.board.getAllActivePieces():
        #     print(piece.getColor()+" "+piece.__class__.__name__+", "+str(piece.getCoordinates()))
        ideallyQueen = game.board.getSquare(5,6).piece
        self.assertEqual(ideallyQueen.__class__.__name__,"Queen")
        return
    def testIsKingInCheck(self):
        self.assertEqual(self.game.board.whichKingInCheck, "black")
    def testMoveListAndNotation(self):
        self.game.displayMoveList()
        self.assertEqual(self.game.moveList[0].notation, "e4")
        self.assertEqual(self.game.moveList[4].notation, "Qxf7+")

class TestAmbiguousMoves(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
        # Plays 1. d3 d6 2. Nf3 Nf6 3. Nbd2 Nbd7 4. Nd4 Nd5 5. N2b3 N7b6
        print(self.game.makeMoveUsingNotation("d3"))
        print(self.game.makeMoveUsingNotation("d6"))
        print(self.game.makeMoveUsingNotation("Nf3"))
        print(self.game.makeMoveUsingNotation("Nf6"))
        print(self.game.makeMove([1,0],[3,1]))
        print(self.game.makeMove([1,7],[3,6]))
        print(self.game.makeMoveUsingNotation("Nd4"))
        print(self.game.makeMoveUsingNotation("Nd5"))
        print(self.game.makeMove([3,1],[1,2]))
        print(self.game.makeMove([3,6],[1,5]))
    def testAmbiguousMoves(self):
        print(self.game.moveList[4].notation)
        self.assertEqual(self.game.moveList[4].notation,"Nbd2")
        self.assertEqual(self.game.moveList[8].notation,"N2b3")


if __name__ == '__main__':
    unittest.main()