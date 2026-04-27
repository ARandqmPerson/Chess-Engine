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
        game.makeMoveCoordinates([4,1],[4,3])
        self.assertNotEqual(board.getSquare(4,3).piece,None)
        self.assertEqual(board.getSquare(4,1).piece,None)
        self.assertEqual(game.moveNumber,1)
        self.assertEqual(game.whoseMove,"black")

class TestMultipleMoves(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
        self.game.makeMoves(("e4","e5","Qh5","Nf6","Qxf7+"))
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
        self.game.makeMoves(("d3","d6","Nf3","Nf6","Nbd2","Nbd7","Nd4","Nd5","N2b3","N7b6"))

class TestEnPassant(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
    # Tests whether en passant is correctly recognized as valid and played
    # and whether it's correctly recognized as invalid
    def testEnPassant(self):
        self.game.makeMoves(("e4","e6","e5","d5","exd6"))
        self.assertEqual(self.board.getSquare(3,5).piece.type,"p")
        self.assertEqual(self.board.getSquare(3,4).piece,None)

class TestCastling(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
        self.game.makeMoves(("e4","d5","exd5","Qxd5","d4","Nc6","Nf3","Bg4","Be2","e6"))
    def testCastlingKingside(self):
        self.game.makeMove("O-O")
        self.assertEqual(self.board.getSquare(notation="g1").piece.type, "k")
        self.assertEqual(self.board.getSquare(notation="f1").piece.type, "r")
    def testCastlingQueenside(self):
        self.game.makeMove("Be3")
        self.game.makeMove("O-O-O")
        self.assertEqual(self.board.getSquare(notation="c8").piece.type, "k")
        self.assertEqual(self.board.getSquare(notation="d8").piece.type, "r")
    def testInvalidCastling(self):
        # Castling should not be valid after the rooks move
        self.game.makeMoves(("Rg1","Rb8","Rh1","Ra8","O-O","O-O-O"))
        self.assertEqual(self.board.getSquare(notation="e8").piece.type, "k")
        self.assertEqual(self.board.getSquare(notation="e1").piece.type, "k")
    def testCastlingThroughCheck(self):
        # The bishop covers f1 and the knight covers d8, 
        # so castling should be invalid
        self.game.makeMoves(("g3","Bh3","Ne5","g6","Nxc6","O-O-O","O-O"))
        self.assertEqual(self.board.getSquare(notation="e8").piece.type, "k")
        self.assertEqual(self.board.getSquare(notation="e1").piece.type, "k")

class TestPromotion(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
    def testStandardPromotionWhite(self):
        self.game.makeMoves(("e4","d5","exd5","c6","dxc6","h6","cxb7","Nc6","b8=Q"))
        self.assertTrue(self.board.getSquare(notation="b8").piece.type == "q")
        self.game.makeMoves(("Bb7","Qxb7"))
        self.assertTrue(self.board.getSquare(notation="b7").piece.type == "q")
        pass
    def testStandardPromotionBlack(self):
        self.game.makeMoves(("e4","d5","f3","dxe4","Na3","exf3","Nb1","fxg2","Nh3","g1=Q"))
        self.assertTrue(self.board.getSquare(notation="g1").piece.type == "q")
        self.game.makeMoves(("Ng5","Qxh1"))
        self.assertTrue(self.board.getSquare(notation="h1").piece.type == "q")
        pass
    def testCapturePromotionWhite(self):
        self.game.makeMoves(("e4","d5","exd5","c6","dxc6","h6","cxb7","Nc6","bxc8=Q"))
        self.assertTrue(self.board.getSquare(notation="c8").piece.type == "q")
        self.game.makeMoves(("Rb8","Qxb8"))
        self.assertTrue(self.board.getSquare(notation="b8").piece.type == "q")
    def testCapturePromotionBlack(self):
        self.game.makeMoves(("e4","d5","f3","dxe4","Na3","exf3","Nb1","fxg2","Nh3","gxh1=Q"))
        self.assertTrue(self.board.getSquare(notation="h1").piece.type == "q")
        self.game.makeMoves(("Ng1","Qxg1"))
        self.assertTrue(self.board.getSquare(notation="g1").piece.type == "q")
        pass

class TestGameEnd(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
    def testCheckmateWhite(self):
        self.game.makeMoves(("e4","e5","Qh5","Nc6","Bc4","Nf6","Qxf7"))
        self.assertEqual(self.game.gameOver,1)
    def testCheckmateBlack(self):
        self.game.makeMoves(("f4","e5","g4","Qh4"))
        self.assertEqual(self.game.gameOver,1)

class TestFEN(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board
    def testPieceSetup(self):
        # This is the FEN after 1. e4
        string = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        self.board.importFEN(string)
        self.assertTrue(self.board.getSquare(notation="e4").pieceColor=="white")
        self.assertTrue(self.board.getSquare(notation="e8").pieceColor=="black")
    def testEnPassant(self):
        # FEN after 1. e4 e6 2. e5 d5
        self.board.importFEN("rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3")
        self.game.makeMove("exd6")
        self.assertTrue(self.board.getSquare(notation="d6").pieceColor=="white")
    def test50MoveRule(self):
        # Each side has king+rook and 98 half-moves have been played without capture/pawn move
        self.board.importFEN("8/8/3kr3/8/8/5KR1/8/8 w - - 98 64")
        self.game.makeMoves(("Rg1","Re8"))
        # Should be draw by 50-move rule
        self.assertTrue(self.game.gameOver == 5)
    def testValidCastling(self):
        self.board.importFEN("r3k2r/ppp2ppp/Qb4qn/b4B1N/7n/1BN5/PPP2PPP/R3K2R w KQkq - 0 1")
        self.assertTrue(self.game.makeMove("O-O"))
        self.assertTrue(self.game.makeMove("O-O"))
    def testInvalidCastling(self):
        self.board.importFEN("r3k2r/ppp2ppp/Qb4qn/b4B1N/7n/1BN5/PPP2PPP/R3K2R w - - 0 1")
        self.assertFalse(self.game.makeMove("O-O"))
        self.assertFalse(self.game.makeMove("O-O"))
        self.board.importFEN("r3k2r/ppp2ppp/Qb4qn/b4B1N/7n/1BN5/PPP2PPP/R3K2R w Kq - 0 1")
        self.assertFalse(self.game.makeMove("O-O-O"))
        self.assertTrue(self.game.makeMove("O-O"))
    def testExportFEN(self):
        self.game.makeMoves(("Nf3","Nf6","Nc3","Nc6","Rg1","Rb8","Rh1","Ra8","e4"))
        result = self.board.exportFEN()
        print("\n"+result)
        print("Expected:\n"+"r1bqkb1r/pppppppp/2n2n2/8/4P3/2N2N2/PPPP1PPP/R1BQKB1R b Qk e3 0 5")
        self.assertEqual(result,"r1bqkb1r/pppppppp/2n2n2/8/4P3/2N2N2/PPPP1PPP/R1BQKB1R b Qk e3 0 5")


if __name__ == '__main__':
    unittest.main()