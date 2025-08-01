class Game:
    def __init__(self, moveNumber=1, whoseMove="white", board=None):
        self.moveNumber = moveNumber
        self.whoseMove = whoseMove
        if board == None:
            self.board = Board(self)
        else:
            self.board = board
        return
    
    def getBoard(self):
        return self.board
    
    def getMoveNumber(self):
        return self.moveNumber
    
    def getWhoseMove(self):
        return self.whoseMove
    # Input the coordinates of the square you want to move from
    # and the square you want to move to
    # For example, starting with makeMove([4,1],[4,3]) is pawn to e4
    def makeMove(self, squareFromCoords, squareToCoords):
        fromX = squareFromCoords[0]
        fromY = squareFromCoords[1]
        toX = squareToCoords[0]
        toY = squareToCoords[1]
        squareFrom = self.board.getSquare(fromX, fromY)
        squareTo = self.board.getSquare(toX, toY)
        valid = False
        for m in self.board.getAllValidMoves():
            if m.getFromSquare()==squareFrom and m.getToSquare()==squareTo:
                move = m
                print(move.getPiece().__class__.__name__+", "+str(squareFromCoords)+"-"+str(squareToCoords))
                valid = True
        if valid == False:
            return "Invalid move"
        self.board.makeMove(move)
        if self.whoseMove == "white":
            self.whoseMove = "black"
        else:
            self.moveNumber += 1
            self.whoseMove = "white"
        self.board.generateAllValidMovesAndThreats()
        return "Valid move"

class Board:
    def __init__(self, game=None):
        self.game = game
        self.capturedPieces = []
        # [0,0] corresponds to a1; [7,0] is h1; [0,7] is a8, etc.
        self.squares = {(i,j): Square((i,j),board=self) for i in range(8) for j in range(8)}
        self.setPieces({(0,0),(7,0)}, Rook, "white")
        self.setPieces({(0,7),(7,7)}, Rook, "black")
        self.setPieces({(1,0),(6,0)}, Knight, "white")
        self.setPieces({(1,7),(6,7)}, Knight, "black")
        self.setPieces({(2,0),(5,0)}, Bishop, "white")
        self.setPieces({(2,7),(5,7)}, Bishop, "black")
        self.setPieces({(3,0)}, Queen, "white")
        self.setPieces({(3,7)}, Queen, "black")
        self.setPieces({(4,0)}, King, "white")
        self.setPieces({(4,7)}, King, "black")
        self.setPieces({(k,1) for k in range(8)}, Pawn, "white")
        self.setPieces({(k,6) for k in range(8)}, Pawn, "black")
        # These will be used to determine checks, checkmates, and stalemates
        self.whiteKing = self.getSquare(4,0).getPiece()
        self.blackKing = self.getSquare(4,7).getPiece()
        self.generateAllValidMovesAndThreats()
        return
    
    def setPieces(self, coordsSet, pieceType, color):
        for i,j in coordsSet:
            piece = pieceType(color=color,square=self.getSquare(i,j),board=self)
            self.getSquare(i,j).setPiece(piece)
        return
    

    def getSquare(self, targetX, targetY):
        return self.squares.get((targetX,targetY))
    
    def getAllSquares(self):
        allSquares = []
        for coords,square in self.squares.items():
            allSquares.append(square)
        return allSquares
    
    def getKing(self, color):
        return self.whiteKing if color == "white" else self.blackKing

    def getAllActivePieces(self, color=None):
        if color != None:
            return [square.getPiece() for square in self.getAllSquares() if square.getPiece()!=None and square.getPiece().getColor()==color]
        return [square.getPiece() for square in self.getAllSquares() if square.getPiece()!=None]
    # Updates valid moves and threats of all pieces
    def generateAllValidMovesAndThreats(self):
        self.allValidMoves = []
        self.allThreatenedMoves = []
        for piece in self.getAllActivePieces():
            piece.generateValidMovesAndThreats()
            self.allValidMoves += piece.getValidMoves()
            self.allThreatenedMoves += piece.getThreatenedMoves()
        return
    
    def getAllValidMoves(self, color=None):
        if color == None:
            return self.allValidMoves
        return [move for move in self.allValidMoves if move.getPiece().getColor()==color]

    def getAllThreatenedMoves(self, color=None):
        if color == None:
            return self.allThreatenedMoves
        return [move for move in self.allThreatenedMoves if move.getPiece().getColor()==color]

    def makeMove(self, move):
        if move.getMoveType() == 1:
            pieceCaptured = move.getPieceCaptured()
            pieceCaptured.setSquare(None)
            pieceCaptured.setStatus(1)
            self.capturedPieces.append(pieceCaptured)
            move.getToSquare().setPiece(move.getPiece())
        elif move.getMoveType() == 0:
            move.getFromSquare().setPiece(None)
            move.getPiece().setSquare(move.getToSquare())
            move.getToSquare().setPiece(move.getPiece())
        return
    
    def undoMove(self, move, moveSet=None):
        if move.getMoveType() == 1:
            pieceCaptured = move.getPieceCaptured()
            pieceCaptured.setSquare(move.getToSquare())
            pieceCaptured.setStatus(0)
            self.capturedPieces.remove(pieceCaptured)
            move.getToSquare().setPiece(pieceCaptured)
        elif move.getMoveType() == 0:
            move.getFromSquare().setPiece(move.getPiece())
            move.getPiece().setSquare(move.getFromSquare())
            move.getToSquare().setPiece(None)
        return

class Square:
    def __init__(self, coordinates=None, piece=None, board=None):
        self.piece = piece
        self.coordinates = coordinates
        self.board = board
        # x and y variables for convenience
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]
        return
    def setCoordinates(self, c):
        self.coordinates = c
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]
        return
    def setPiece(self, p):
        self.piece = p
        return
    def getPiece(self):
        return self.piece
    def getPieceColor(self):
        if self.piece is not None:
            return self.piece.getColor()
        else:
            return None
    def getCoordinates(self):
        return self.coordinates
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getBoard(self):
        return self.board
    def setBoard(self, b):
        self.board = b
        return
# Move types: 0=Normal move, 1=capture, 2=castling, 3=promotion, 4=en passant, 5=threat
class Move:
    def __init__(self, pieceMoved=None, fromSquare=None, toSquare=None, moveType=None):
        self.piece = pieceMoved
        self.fromSquare = fromSquare
        self.toSquare = toSquare
        self.moveType = moveType
        self.pieceColor = self.piece.getColor()
        self.board = self.piece.getBoard()
        self.game = self.board.game
        self.pieceCaptured = toSquare.getPiece() if moveType == 1 else None

    def setMoveType(self, t):
        self.moveType = t
        return
    
    def getMoveType(self):
        return self.moveType
    
    def setPiece(self, p):
        self.piece = p
        return

    def getPiece(self):
        return self.piece
    
    def getPieceCaptured(self):
        return self.pieceCaptured
    
    def getFromSquare(self):
        return self.fromSquare
    
    def getToSquare(self):
        return self.toSquare
    # After this move is made, checks which enemy pieces previously threatened the square that
    # the king is currently on; then regenerates their moves to see if they still threaten it
    def leavesKingInCheck(self):
        result = False
        king = self.board.getKing(self.piece.getColor())
        oppositeColor = "white" if self.piece.getColor()=="black" else "black"
        kingSquare = king.getSquare()
        threateningPieces = []
        for move in self.board.getAllThreatenedMoves(oppositeColor):
            if move.getToSquare() == kingSquare:
                threateningPieces.append(move.getPiece())
        self.board.makeMove(self)
        for piece in threateningPieces:
            piece.generateValidMovesAndThreats(True)
            for m in piece.getValidMoves():
                if m.getToSquare()==kingSquare:
                    result = True
        self.board.undoMove(self)
        return result
    

class Piece:
    def __init__(self, color=None, square=None, board=None, status=None):
        self.color = color
        self.square = square
        self.x = self.square.getX()
        self.y = self.square.getY()
        self.board = board
        self.validMoves = []
        self.threatenedMoves = []
        # 0 when on the board, 1 when captured
        self.status = 0
        return
    def getValidMoves(self):
        return self.validMoves
    # Returns only the coordinates that can be moved to
    def getValidMoveCoordinates(self):
        return [i.getToSquare().getCoordinates() for i in self.validMoves]
    def getThreatenedMoves(self):
        return self.threatenedMoves
    def getThreatenedSquareCoordinates(self):
        return [i.getToSquare().getCoordinates() for i in self.threatenedMoves]
    def getColor(self):
        return self.color
    def setColor(self, c):
        self.color = c
        return
    def getSquare(self):
        return self.square
    def setSquare(self, s):
        self.square = s
        if s != None:
            self.x = self.square.getX()
            self.y = self.square.getY()
        return
    def getCoordinates(self):
        return self.square.getCoordinates()
    def getBoard(self):
        return self.board
    def setBoard(self, b):
        self.board = b
        return
    def getStatus(self):
        return self.status
    def setStatus(self, s):
        self.status = s
        if s == 1:
            self.square = None
        return
    
class Pawn(Piece):
    def __init__(self, firstMoveStatus=0, color=None, square=None, board=None):
        super().__init__(color, square, board)
        # 0 if pawn hasn't been moved, 1 if it just moved and en passant is possible,
        # and 2 if it has moved and en passant is not possible
        self.firstMoveStatus = firstMoveStatus
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedMoves = []
        # Determines which way pawn is moving
        if self.color == "white":
            inc = 1
        else:
            inc = -1

        if board.getSquare(self.x, self.y+inc).piece == None:
            self.validMoves.append(Move(self, square, board.getSquare(self.x, self.y+inc), 0))
            if board.getSquare(self.x, self.y+2*inc).piece == None and self.firstMoveStatus == 0:
                self.validMoves.append(Move(self, square, board.getSquare(self.x, self.y+2*inc), 0))
        if self.x!=0:
            current = board.getSquare(self.x-1,self.y+inc)
            self.threatenedMoves.append(Move(self, square, current, 5))
            if current.getPiece() not in (None,self.color):
                self.validMoves.append(Move(self,square,current,1))
        if self.x!=7:
            current = board.getSquare(self.x+1,self.y+inc)
            self.threatenedMoves.append(Move(self, square, current, 5))
            if current.getPiece() not in (None,self.color):
                self.validMoves.append(Move(self,square,current,1))
        if not repeat:
            for move in self.validMoves:
                if move.leavesKingInCheck():
                    print("test2")
                    self.validMoves.remove(move)
        return

class Rook(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        return
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedMoves = []
        # Reused and adapted code from Bishop class
        for i, j in {(0,1),(0,-1),(1,0),(-1,0)}:
            blocked = False
            inc = 1
            while 0<=self.x+i*inc<=7 and 0<=self.y+j*inc<=7:
                current = board.getSquare(self.x+i*inc,self.y+j*inc)
                self.threatenedMoves.append(Move(self, square, current, 5))
                if not blocked:
                    if current.getPieceColor() == None:
                        self.validMoves.append(Move(self,square,current,0))
                    elif current.getPieceColor() != self.color:
                        blocked = True
                        self.validMoves.append(Move(self,square,current,1))
                    else:
                        blocked = True
                inc += 1
        if not repeat:
            for move in self.validMoves:
                if move.leavesKingInCheck():
                    self.validMoves.remove(move)
        return

class Knight(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        return
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedMoves = []
        self.potentialCoordinates = [(self.x+1,self.y+2),(self.x-1,self.y+2),(self.x+2,self.y+1),(self.x-2,self.y+1),(self.x+2,self.y-1),(self.x-2,self.y-1),(self.x+1,self.y-2),(self.x-1,self.y-2)]
        self.possibleSquares = [board.getSquare(i,j) for (i,j) in self.potentialCoordinates if -1<i<8 and -1<j<8]
        for i in self.possibleSquares:
            self.threatenedMoves.append(Move(self, square, i, 5))
            if i.getPiece() == None:
                self.validMoves.append(Move(self, square, i, 0))
            elif i.getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self, square, i, 1))
        if not repeat:
            for move in self.validMoves:
                if move.leavesKingInCheck():
                    self.validMoves.remove(move)
        return

class Bishop(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        return 
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedMoves = []
        for i, j in {(1,1),(1,-1),(-1,1),(-1,-1)}:
            blocked = False
            inc = 1
            while 0<=self.x+i*inc<=7 and 0<=self.y+j*inc<=7:
                current = board.getSquare(self.x+i*inc,self.y+j*inc)
                self.threatenedMoves.append(Move(self, square, current, 5))
                if not blocked:
                    if current.getPieceColor() == None:
                        self.validMoves.append(Move(self,square,current,0))
                    elif current.getPieceColor() != self.color:
                        blocked = True
                        self.validMoves.append(Move(self,square,current,1))
                    else:
                        blocked = True
                inc += 1
        if not repeat:
            for move in self.validMoves:
                if move.leavesKingInCheck():
                    self.validMoves.remove(move)
        return

class Queen(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        # Hidden bishop and rook objects used for generateValidMovesAndThreats
        self.bishop = Bishop(self.getColor(),self.getSquare(),self.board)
        self.rook = Rook(self.getColor(),self.getSquare(),self.board)
        return
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedMoves = []
        self.bishop.setSquare(square)
        self.rook.setSquare(square)
        self.bishop.generateValidMovesAndThreats(repeat)
        self.rook.generateValidMovesAndThreats(repeat)
        for move in self.bishop.getValidMoves() + self.rook.getValidMoves():
            move.setPiece(self)
            self.validMoves.append(move)
        for move in self.bishop.getThreatenedMoves() + self.rook.getThreatenedMoves():
            move.setPiece(self)
            self.threatenedMoves.append(move)
        if not repeat:
            for move in self.validMoves:
                if move.leavesKingInCheck():
                    self.validMoves.remove(move)
        return

class King(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        self.hasMoved = False
        return
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedMoves = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                current = board.getSquare(self.x+i,self.y+j)
                if current == None:
                    break
                self.threatenedMoves.append(Move(self, square, current, 5))
                if current.getPiece() == None:
                    self.validMoves.append(Move(self,square,current,0))
                elif current.getPiece().getColor() != self.getColor():
                    self.validMoves.append(Move(self,square,current,1))
        if not repeat:
            for move in self.validMoves:
                if move.leavesKingInCheck():
                    self.validMoves.remove(move)
        return