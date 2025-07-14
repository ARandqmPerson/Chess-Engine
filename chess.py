class Game:
    def __init__(self, moveNumber=1, whoseMove='white', board=None):
        self.moveNumber = moveNumber
        self.whoseMove = whoseMove
        if board == None:
            self.board = Board(self)
        else:
            self.board = board
        return
    
    def getBoard(self):
        return self.board

class Board:
    def __init__(self, game=None):
        self.game = game
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
        self.generateAllValidMovesAndThreats()
        # These will be used to determine checks, checkmates, and stalemates
        self.whiteKing = self.getSquare(4,0).getPiece()
        self.blackKing = self.getSquare(4,7).getPiece()
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
    
    def getAllPieces(self):
        allPieces = []
        for square in self.getAllSquares():
            if square.getPiece() != None:
                allPieces.append(square.getPiece())
        return allPieces
    
    def generateAllValidMovesAndThreats(self):
        self.allValidMoves = []
        self.allThreatenedSquares = []
        for piece in self.getAllPieces():
            piece.generateValidMovesAndThreats()
            self.allValidMoves += piece.getValidMoves()
            self.allThreatenedSquares += piece.getThreatenedSquares()
        return
    
    def getAllValidMoves(self):
        return self.allValidMoves

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

class Move:
    def __init__(self, pieceMoved=None, fromSquare=None, toSquare=None, moveType=None):
        self.piece = pieceMoved
        self.fromSquare = fromSquare
        self.toSquare = toSquare
        self.moveType = moveType
        self.pieceColor = self.piece.getColor()
        self.board = self.piece.getBoard()

    def setMoveType(self, t):
        self.moveType = t
        return
    
    def getMoveType(self):
        return self.moveType
    
    def getPieceMoved(self):
        return self.piece
    
    def getFromSquare(self):
        return self.fromSquare
    
    def getToSquare(self):
        return self.toSquare
    # Used to determine legality
    def leavesKingInCheck(self):
        # TODO
        return
    

class Piece:
    def __init__(self, color=None, square=None, board=None):
        self.color = color
        self.square = square
        self.x = self.square.getX()
        self.y = self.square.getY()
        self.board = board
        self.validMoves = []
        self.threatenedSquares = []
        return
    def getValidMoves(self):
        return self.validMoves
    # Returns only the coordinates that can be moved to
    def getValidMoveCoordinates(self):
        return [i.getToSquare().getCoordinates() for i in self.validMoves]
    def getThreatenedSquares(self):
        return self.threatenedSquares
    def getThreatenedSquareCoordinates(self):
        return [i.getCoordinates() for i in self.threatenedSquares]
    def getColor(self):
        return self.color
    def setColor(self, c):
        self.color = c
        return
    def getSquare(self):
        return self.square
    def setSquare(self, s):
        self.square = s
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
    
class Pawn(Piece):
    def __init__(self, firstMoveStatus=0, color=None, square=None, board=None):
        super().__init__(color, square, board)
        # 0 if pawn hasn't been moved, 1 if it just moved and en passant is possible,
        # and 2 if it has moved and en passant is not possible
        self.firstMoveStatus = firstMoveStatus
    def generateValidMovesAndThreats(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedSquares = []
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
            self.threatenedSquares.append(current)
            if current.getPiece() not in (None,self.color):
                self.validMoves.append(self,square,current,1)
        if self.x!=7:
            current = board.getSquare(self.x+1,self.y+inc)
            self.threatenedSquares.append(current)
            if current.getPiece() not in (None,self.color):
                self.validMoves.append(self,square,current,1)
        return

class Rook(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        return
    
    def generateValidMovesAndThreats(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedSquares = []
        # Reused and adapted code from Bishop class
        for i, j in {(0,1),(0,-1),(1,0),(-1,0)}:
            blocked = False
            inc = 1
            while 0<=self.x+i*inc<=7 and 0<=self.y+j*inc<=7:
                current = board.getSquare(self.x+i*inc,self.y+j*inc)
                self.threatenedSquares.append(current)
                if not blocked:
                    if current.getPieceColor() == None:
                        self.validMoves.append(Move(self,square,current,0))
                    elif current.getPieceColor() != self.color:
                        blocked = True
                        self.validMoves.append(Move(self,square,current,1))
                    else:
                        blocked = True
                inc += 1
        return

class Knight(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        return
    
    def generateValidMovesAndThreats(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedSquares = []
        self.potentialCoordinates = [(self.x+1,self.y+2),(self.x-1,self.y+2),(self.x+2,self.y+1),(self.x-2,self.y+1),(self.x+2,self.y-1),(self.x-2,self.y-1),(self.x+1,self.y-2),(self.x-1,self.y-2)]
        self.possibleSquares = [board.getSquare(i,j) for (i,j) in self.potentialCoordinates if -1<i<8 and -1<j<8]
        for i in self.possibleSquares:
            self.threatenedSquares.append(i)
            if i.getPiece() == None:
                self.validMoves.append(Move(self, square, i, 0))
            elif i.getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self, square, i, 1))
        return

class Bishop(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        return 
    
    def generateValidMovesAndThreats(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedSquares = []
        for i, j in {(1,1),(1,-1),(-1,1),(-1,-1)}:
            blocked = False
            inc = 1
            while 0<=self.x+i*inc<=7 and 0<=self.y+j*inc<=7:
                current = board.getSquare(self.x+i*inc,self.y+j*inc)
                self.threatenedSquares.append(current)
                if not blocked:
                    if current.getPieceColor() == None:
                        self.validMoves.append(Move(self,square,current,0))
                    elif current.getPieceColor() != self.color:
                        blocked = True
                        self.validMoves.append(Move(self,square,current,1))
                    else:
                        blocked = True
                inc += 1
        return

class Queen(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        # Hidden bishop and rook objects used for generateValidMovesAndThreats
        self.bishop = Bishop(self.getColor(),self.getSquare(),self.board)
        self.rook = Rook(self.getColor(),self.getSquare(),self.board)
        return
    
    def generateValidMovesAndThreats(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedSquares = []
        self.bishop.setSquare(square)
        self.rook.setSquare(square)
        self.validMoves += self.bishop.getValidMoves()
        self.validMoves += self.rook.getValidMoves()
        self.threatenedSquares += self.bishop.getThreatenedSquares()
        self.threatenedSquares += self.rook.getThreatenedSquares()
        return

class King(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        self.hasMoved = False
        return
    
    def generateValidMovesAndThreats(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.threatenedSquares = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                current = board.getSquare(self.x+i,self.y+j)
                if current == None:
                    break
                self.threatenedSquares.append(current)
                if current.getPiece() == None:
                    self.validMoves.append(Move(self,square,current,0))
                elif current.getPiece().getColor() != self.getColor():
                    self.validMoves.append(Move(self,square,current,1))
        return