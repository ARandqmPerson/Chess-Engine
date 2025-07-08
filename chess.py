LETTERS = ['a','b','c','d','e','f','g','h']

class Game:
    def __init__(self, moveNumber=1, whoseMove='w', currentBoard=None):
        self.moveNumber = moveNumber
        self.whoseMove = whoseMove
        self.currentBoard = currentBoard
        return

class Board:
    def __init__(self):
        # [0,0] corresponds to a1; [0,7] is h1; [7,0] is a8, etc.
        self.squares = [[Square([i, j]) for i in range(8)] for j in range(8)]
        self.setPieces(([0,0],[0,7]),"Rook", "white")
        self.setPieces(([7,0],[7,7]),"Rook", "black")
        self.setPieces(([0,1],[0,6]), "Knight", "white")
        self.setPieces(([7,1],[7,6]), "Knight", "black")
        self.setPieces(([0,2],[0,5]), "Bishop", "white")
        self.setPieces(([7,2],[7,5]), "Bishop", "black")
        self.setPieces(([0,3]), "Queen", "white")
        self.setPieces(([7,3]), "Queen", "black")
        self.setPieces(([0,4]), "King", "white")
        self.setPieces(([7,4]), "King", "black")
        self.setPieces(([1,k] for k in range(8)), Pawn(), "white")
        self.setPieces(([6,k] for k in range(8)), Pawn(), "black")
        # These will be used to determine checks, checkmates, and stalemates
        self.whiteKing = self.getSquare(0,4).getPiece()
        self.blackKing = self.getSquare(7,4).getPiece()
        return
    
    def setPieces(self, coordsSet, piece, color):
        for i, j in coordsSet:
            self.getSquare(i, j).setPiece(piece)
            piece.setColor(color)
            piece.setSquare(self.getSquare(i, j))
        return
    
    def getSquare(self, targetX, targetY):
        return self.squares[targetX][targetY]
    

class Square:
    def __init__(self, piece=None, coordinates=None):
        self.piece = piece
        self.coordinates = coordinates
        return
    def setCoordinates(self, c):
        self.coordinates = c
        # x and y variables for convenience
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]
        return
    def setPiece(self, p):
        self.piece = p
        return
    def getPiece(self):
        return self.piece
    def getCoordinates(self):
        return self.coordinates
    def getX(self):
        return self.x
    def getY(self):
        return self.y

class Move:
    def __init__(self, pieceMoved=None, fromSquare=None, toSquare=None, moveType=None):
        self.piece = pieceMoved
        self.fromSquare = fromSquare
        self.toSquare = toSquare
        self.moveType = moveType

    def leavesKingInCheck(self, board):
        if self.pieceMoved.getColor() == "white":
            currentKing = board.whiteKing
            oppositeSide = "black"
        else:
            currentKing = board.blackKing
            oppositeSide = "white"
        
        return

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
    def __init__(self, color=None, square=None):
        self.color = color
        self.square = square
        return
    def getColor(self):
        return self.color
    def setColor(self, c):
        self.color = c
        return
    def getSquare(self):
        return self.square
    def setSquare(self, s):
        self.square = s
        self.x = self.square.x
        self.y = self.square.y
        return
    
class Pawn(Piece):
    def __init__(self, firstMoveStatus=0):
        super().__init__()
        # 0 if pawn hasn't been moved, 1 if it just moved and en passant is possible,
        # and 2 if it has moved and en passant is not possible
        self.firstMoveStatus = firstMoveStatus
    def getValidMoves(self, board):
        self.validMoves = []
        # Determines which way pawn is moving
        if self.color == "white":
            self.inc = 1
        else:
            self.inc = -1

        # Adds all possible moves
        if board.getSquare(self.x, self.y+self.inc).piece == None:
            self.validMoves.append(Move(self, self.square, board.getSquare(self.x, self.y+self.inc), 0))
            if board.getSquare(self.x, self.y+2*self.inc).piece == None and self.firstMoveStatus == 0:
                self.validMoves.append(Move(self, self.square, board.getSquare(self.x, self.y+2*self.inc), 0))
        if board.getSquare(self.x+1, self.y+self.inc).piece != None and board.getSquare(self.x+1, self.y+self.inc).piece.color != self.color:
            self.validMoves.append(Move(self, self.square, board.getSquare(self.x+1, self.y+self.inc), 1))
        if board.getSquare(self.x-1, self.y+self.inc).piece != None and board.getSquare(self.x-1, self.y+self.inc).piece.color != self.color:
            self.validMoves.append(Move(self, self.square, board.getSquare(self.x-1, self.y+self.inc), 1))
        return self.validMoves

class Rook(Piece):
    def __init__(self):
        super().__init__()
        return
    
    def getValidMoves(self, board):
        self.validMoves = []
        for i in range(0-self.y, 7-self.y):
            if board.getSquare(self.x,self.y+i).getPiece() == None:
                self.validMoves.append(Move(self.getSquare(),board.getSquare(self.x,self.y+i),0))
            elif board.getSquare(self.x,self.y+i).getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self.getSquare(),board.getSquare(self.x,self.y+i),1))
        for j in range(0-self.x, 7-self.x):
            if board.getSquare(self.x+j,self.y).getPiece() == None:
                self.validMoves.append(Move(self.getSquare(),board.getSquare(self.x+j,self.y),0))
            elif board.getSquare(self.x+j,self.y).getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self.getSquare(),board.getSquare(self.x+j,self.y),1))
        return self.validMoves

class Knight(Piece):
    def __init__(self):
        super().__init__()
        return
    
    def getValidMoves(self, board):
        self.validMoves = []
        self.potentialCoordinates = [(self.x+1,self.y+2),(self.x-1,self.y+2),(self.x+2,self.y+1),(self.x-2,self.y+1),(self.x+2,self.y-1),(self.x-2,self.y-1),(self.x+1,self.y-2),(self.x-1,self.y-2)]
        self.possibleSquares = [board.getSquare(i,j) for (i,j) in self.potentialCoordinates if -1<i<8 and -1<j<8]
        for i in self.possibleSquares:
            if i.getPiece() == None:
                self.validMoves.append(Move(self.getSquare(), i, 0))
            elif i.getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self.getSquare(), i, 1))
        return

class Bishop(Piece):
    def __init__(self):
        super().__init__()
        return
    
    def getValidMoves(self, board):
        self.validMoves = []
        self.possibleSquares = []
        for i in range(8):
            if -1<self.y+(self.x-i)<8:
                self.possibleSquares.append(board.getSquare(i,self.y+(self.x-i)))
            if -1<self.y-(self.x-i)<8:
                self.possibleSquares.append(board.getSquare(i,self.y-(self.x-i)))
        for j in self.possibleSquares:
            if j.getPiece() == None:
                self.validMoves.append(Move(self.getSquare(),j,0))
            elif j.getPiece().getColor() != self.getColor():
                self.validMoves.append(Move(self.getSquare(),j,1))
        return self.validMoves

class Queen(Piece):
    def __init__(self):
        super().__init__()
        # Hidden bishop and rook objects used for getValidMoves
        self.bishop = Bishop(self.getColor(),self.getSquare())
        self.rook = Rook(self.getColor(),self.getSquare())
        return
    
    def getValidMoves(self, board):
        self.bishop.setSquare(self.getSquare())
        self.rook.setSquare(self.getSquare())
        self.validMoves = []
        self.validMoves += Bishop.getValidMoves(board)
        self.validMoves += Rook.getValidMoves(board)
        return self.validMoves

class King(Piece):
    def __init__(self):
        super().__init__()
        self.hasMoved = False
        return
    
    def getValidMoves(self, board):
        self.validMoves = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if board.getSquare(i,j).getPiece() == None:
                    self.validMoves.append(Move(self.getSquare(),board.getSquare(i,j),0))
                elif board.getSquare(i,j).getPiece().getColor() != self.getColor():
                    self.validMoves.append(Move(self.getSquare(),board.getSquare(i,j),1))
        # Check for castling
        
        return self.validMoves
    
