class Game:
    def __init__(self, moveNumber=1, whoseMove='white', currentBoard=None):
        self.moveNumber = moveNumber
        self.whoseMove = whoseMove
        if currentBoard == None:
            self.currentBoard = Board(self)
        else:
            self.currentBoard = currentBoard
        return
    
    def getCurrentBoard(self):
        return self.currentBoard

class Board:
    def __init__(self, game=None):
        self.game = game
        # [0,0] corresponds to a1; [7,0] is h1; [0,7] is a8, etc.
        self.squares = [[Square([i, j]) for i in range(8)] for j in range(8)]
        self.setPieces({(0,0),(7,0)}, Rook(), "white")
        self.setPieces({(0,7),(7,7)}, Rook(), "black")
        self.setPieces({(1,0),(6,0)}, Knight(), "white")
        self.setPieces({(1,7),(6,7)}, Knight(), "black")
        self.setPieces({(2,0),(5,0)}, Bishop(), "white")
        self.setPieces({(2,7),(5,7)}, Bishop(), "black")
        self.setPieces({(3,0)}, Queen(), "white")
        self.setPieces({(3,7)}, Queen(), "black")
        self.setPieces({(4,0)}, King(), "white")
        self.setPieces({(4,7)}, King(), "black")
        self.setPieces({(1,k) for k in range(8)}, Pawn(), "white")
        self.setPieces({(6,k) for k in range(8)}, Pawn(), "black")
        self.generateAllValidMoves()
        # These will be used to determine checks, checkmates, and stalemates
        self.whiteKing = self.getSquare(4,0).getPiece()
        self.blackKing = self.getSquare(4,7).getPiece()
        return
    
    def setPieces(self, coordsSet, piece, color):
        for i, j in coordsSet:
            self.getSquare(i, j).setPiece(piece)
            piece.setColor(color)
            piece.setSquare(self.getSquare(i, j))
            piece.setBoard(self)
        return
    
    def getSquare(self, targetX, targetY):
        return self.squares[targetX][targetY]
    
    def getAllSquares(self):
        allSquares = []
        for row in self.squares:
            for square in row:
                allSquares.append(square)
        return allSquares
    
    def getAllPieces(self):
        allPieces = []
        for square in self.getAllSquares():
            if square.getPiece() != None:
                allPieces.append(square.getPiece())
        return allPieces
    
    def generateAllValidMoves(self):
        self.allValidMoves = []
        for piece in self.getAllPieces():
            piece.generateValidMoves()
            self.allValidMoves += piece.getValidMoves()
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
    

class Piece:
    def __init__(self, color=None, square=None, board=None):
        self.color = color
        self.square = square
        self.board = board
        self.validMoves = []
        self.threatenedSquares = []
        return
    def getValidMoves(self):
        return self.validMoves
    def getThreatenedSquares(self):
        return self.threatenedSquares
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
    def generateValidMoves(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        # Determines which way pawn is moving
        if self.color == "white":
            self.inc = 1
        else:
            self.inc = -1

        # Adds all possible moves
        if board.getSquare(self.x, self.y+self.inc).piece == None:
            self.validMoves.append(Move(self, square, board.getSquare(self.x, self.y+self.inc), 0))
            if board.getSquare(self.x, self.y+2*self.inc).piece == None and self.firstMoveStatus == 0:
                self.validMoves.append(Move(self, square, board.getSquare(self.x, self.y+2*self.inc), 0))
        if board.getSquare(self.x+1, self.y+self.inc).piece != None and board.getSquare(self.x+1, self.y+self.inc).piece.color != self.color:
            self.validMoves.append(Move(self, square, board.getSquare(self.x+1, self.y+self.inc), 1))
        if board.getSquare(self.x-1, self.y+self.inc).piece != None and board.getSquare(self.x-1, self.y+self.inc).piece.color != self.color:
            self.validMoves.append(Move(self, square, board.getSquare(self.x-1, self.y+self.inc), 1))
        return

class Rook(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        return
    
    def generateValidMoves(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        for i in range(0, 1-self.y, -1):
            current = board.getSquare(self.x,self.y+i)
            if current.getPiece() == None:
                self.validMoves.append(Move(self,square,current,0))
            elif current.getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self,square,current,1))
            else:
                break
        for i in range(0, 8-self.y):
            current = board.getSquare(self.x,self.y+i)
            if current.getPiece() == None:
                self.validMoves.append(Move(self,square,current,0))
            elif current.getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self,square,current,1))
            else:
                break
        for j in range(0, 1-self.x, -1):
            current = board.getSquare(self.x+j,self.y)
            if current.getPiece() == None:
                self.validMoves.append(Move(self,square,current,0))
            elif current.getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self,square,current,1))
            else:
                break
        for j in range(0, 8-self.x):
            current = board.getSquare(self.x+j,self.y)
            if current.getPiece() == None:
                self.validMoves.append(Move(self,square,current,0))
            elif current.getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self,square,current,1))
            else:
                break
        return

class Knight(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        return
    
    def generateValidMoves(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.potentialCoordinates = [(self.x+1,self.y+2),(self.x-1,self.y+2),(self.x+2,self.y+1),(self.x-2,self.y+1),(self.x+2,self.y-1),(self.x-2,self.y-1),(self.x+1,self.y-2),(self.x-1,self.y-2)]
        self.possibleSquares = [board.getSquare(i,j) for (i,j) in self.potentialCoordinates if -1<i<8 and -1<j<8]
        for i in self.possibleSquares:
            if i.getPiece() == None:
                self.validMoves.append(Move(self, square, i, 0))
            elif i.getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self, square, i, 1))
        return

class Bishop(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        return 
    
    def generateValidMoves(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        for i, j in {[1,1],[1,-1],[-1,1],[-1,-1]}:
            while board.getSquare().getPieceColor not in [None, self.getColor()]:
                pass
        return

class Queen(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        # Hidden bishop and rook objects used for generateValidMoves
        self.bishop = Bishop(self.getColor(),self.getSquare(),self.board)
        self.rook = Rook(self.getColor(),self.getSquare(),self.board)
        return
    
    def generateValidMoves(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        self.bishop.setSquare(square)
        self.rook.setSquare(square)
        self.validMoves += self.bishop.getValidMoves()
        self.validMoves += self.rook.getValidMoves()
        return

class King(Piece):
    def __init__(self, color=None, square=None, board=None):
        super().__init__(color, square, board)
        self.hasMoved = False
        return
    
    def generateValidMoves(self):
        board = self.board
        square = self.getSquare()
        self.validMoves = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if board.getSquare(i,j).getPiece() == None:
                    self.validMoves.append(Move(self,square,board.getSquare(i,j),0))
                elif board.getSquare(i,j).getPiece().getColor() != self.getColor():
                    self.validMoves.append(Move(self,square,board.getSquare(i,j),1))
        # Check for castling
        
        return
    
