class Game:
    def __init__(self, moveNumber=1, whoseMove="white", board=None, moves=None):
        self.moveNumber = moveNumber
        self.whoseMove = whoseMove
        self.moveList = [] if moves == None else moves
        self.board = Board(self) if board == None else board
        return
    
    # TODO: Finish getMoveNotation()
    def displayMoveList(self):
        for move in self.moveList:
            print(move.notation)

    # Makes move if valid and returns True if valid and False if not
    def makeMoveCoordinates(self, squareFromCoords, squareToCoords, promotionType=None):
        fromX = squareFromCoords[0]
        fromY = squareFromCoords[1]
        toX = squareToCoords[0]
        toY = squareToCoords[1]
        squareFrom = self.board.getSquare(fromX, fromY)
        squareTo = self.board.getSquare(toX, toY)
        valid = False
        for m in self.board.allValidMoves:
            if m.fromSquare==squareFrom and m.toSquare==squareTo and m.promoteTo==promotionType:
                move = m
                valid = True
        if not valid:
            return False
        # Makes the move on the board
        self.moveList.append(move)
        self.board.makeMove(move, True)
        # Print statement for debugging
        # print(str(move.notation)+"; Valid move; Move type: "+str(move.type))
        if self.whoseMove == "black":
            self.moveNumber += 1
        self.whoseMove = "white" if self.whoseMove == "black" else "black"
        self.board.generateAllValidMovesAndThreats(True)
        return True
    
    # Calls makeMoveCoordinates() but accepts standard notation
    def makeMove(self, notation):
        # The user may or may not add a + or # sign to denote check/checkmate,
        # so it's removed if present
        notation1 = notation[0:-1] if notation[-1] in ("+","#") else notation
        for move in self.board.allValidMoves:
            notation2 = move.notation[0:-1] if move.notation[-1] in ("+","#") else move.notation
            if notation1 == notation2:
                return self.makeMoveCoordinates(move.fromSquare.coordinates,move.toSquare.coordinates,move.promoteTo)
        return False
    
    def makeMoves(self, moves):
        for move in moves:
            if not self.makeMove(move):
                return False
        return True

    
class Board:
    def __init__(self, game=None):
        # Similarly to the Game class's moveList, this list keeps track of moves made on the board.
        # One item on the list represents a half-move that has been played. However, the list only tracks
        # which pawn on the board can be captured en passant on any given move. The downside of
        # updating this list is that it must be done every time makeMove() is called, but it's
        # necessary because it otherwise wouldn't be possible to track en passant status after
        # undoMove() is called.
        self.whichPawnMoved2 = []
        # whichPawnMoved2[-1] causes an error when the list is empty
        self.whichPawnMoved2.append(None)
        self.game = game
        self.capturedPieces = []
        self.whichKingInCheck = None
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
        self.whiteKing = self.getSquare(4,0).piece
        self.blackKing = self.getSquare(4,7).piece
        self.generateAllValidMovesAndThreats(True)
        # Only used for easier debugging
        self.squaresNotation = {square.notation: square for square in self.squares.values()}
        return
    
    def setPieces(self, coordsSet, pieceType, color):
        for i,j in coordsSet:
            piece = pieceType(color=color,square=self.getSquare(i,j),board=self)
            self.getSquare(i,j).setPiece(piece)
        return
    
    # Accepts x, y coordinates or standard notation
    def getSquare(self, targetX=None, targetY=None, notation=None):
        if notation != None:
            for square in self.squares:
                if self.squares.get(square).notation == notation:
                    return self.squares.get(square)
        return self.squares.get((targetX,targetY))
    
    def getAllSquares(self):
        allSquares = []
        for coords,square in self.squares.items():
            allSquares.append(square)
        return allSquares
    
    def getKing(self, color):
        return self.whiteKing if color == "white" else self.blackKing

    def updateWhichKingInCheck(self):
        whiteKingSquare = self.whiteKing.square
        blackKingSquare = self.blackKing.square
        for move in self.getAllValidMoves("white"):
            if move.toSquare == blackKingSquare:
                self.whichKingInCheck = "black"
                break
        for move in self.getAllValidMoves("black"):
            if move.toSquare == whiteKingSquare:
                self.whichKingInCheck = "white"
                break
        return

    def getAllActivePieces(self, color=None):
        if color != None:
            return [square.piece for square in self.getAllSquares() if square.pieceColor==color]
        return [square.piece for square in self.getAllSquares() if square.piece!=None]
   
    # Updates valid moves and threats of all pieces
    # color parameter should be "white" or "black" if color is specified
    
    # NOTE: calls generateValidMovesAndThreats() for each piece, which calls
    # updateLeavesKingInCheck(), which calls makeMove() and then generateValidMovesAndThreats() again with repeat=True
    # so that updateLeavesKingInCheck() is not called again, and then undoMove().

    # NOTE: Valid moves depend on the current threatened moves (so that a move does not leave
    # the king on a threatened square), but generateValidMovesAndThreats() sometimes generates all valid
    # moves BEFORE threatened moves, so generateAllValidMovesAndThreats() must be called on all pieces of
    # the opposite color before pieces of the color who may be in check. To do this, 
    # pass threatsFirst as True; if needed, specify whose move it is with the color parameter

    def generateAllValidMovesAndThreats(self, threatsFirst=False, color=None):
        if color == None:
            color = self.game.whoseMove
        self.allValidMoves = []
        self.allThreatenedMoves = []
        if not threatsFirst:
            for piece in self.getAllActivePieces():
                piece.generateValidMovesAndThreats()
                self.allValidMoves += piece.validMoves
                self.allThreatenedMoves += piece.threatenedMoves
        else:
            # Only threatened moves are needed for the opposing side,
            # only valid moves are needed for the side whose turn it is
            for piece in self.getAllActivePieces():
                if piece.color != color:
                    piece.generateValidMovesAndThreats()
                    self.allThreatenedMoves += piece.threatenedMoves
            for piece in self.getAllActivePieces():
                if piece.color == color:
                    piece.generateValidMovesAndThreats()
                    self.allValidMoves += piece.validMoves

        # For debugging purposes; a list of strings corresponding
        # to valid moves
        self.allValidMovesNotation = []
        for move in self.allValidMoves:
            self.allValidMovesNotation.append(move.notation)
        return
    
    def getAllValidMoves(self, color=None):
        if color == None:
            return self.allValidMoves
        return [move for move in self.allValidMoves if move.piece.color==color]
    
    def displayValidMoves(self):
        result = ""
        color = self.game.whoseMove
        for move in self.allValidMoves:
            if move.piece.color == color:
                result += move.notation + ", "
        result = result[0:-2]
        print("Valid moves:\n" + result)
        return


    def getAllThreatenedMoves(self, color=None):
        if color == None:
            return self.allThreatenedMoves
        return [move for move in self.allThreatenedMoves if move.piece.color==color]

    # TODO: Add other move types
    # NOTE: For efficiency, makeMove() only runs 
    # generateAllValidMovesAndThreats and updateWhichKingInCheck() if update is True
    # NOTE: To update notation, disambiguation must be checked BEFORE the move is made,
    # but whether the move is a check can only be determined AFTER it's been made, so it's
    # automatically done when the function updates for check
    def makeMove(self, move, update=False):
        move.updateNotation()
        type = move.type
        if type == 2:
            move.fromSquare.setPiece(None)
            move.toSquare.setPiece(move.piece)
            move.piece.setSquare(move.toSquare)
            # Finds and moves corresponding rook after moving king
            if move.toSquare.x == 6:
                rook = self.getSquare(7,move.toSquare.y).piece
                target = self.getSquare(5,move.toSquare.y)
            else:
                rook = self.getSquare(0,move.toSquare.y).piece
                target = self.getSquare(3,move.toSquare.y)
            rook.square.setPiece(None)
            rook.setSquare(target)
            target.setPiece(rook)
        if type in (1,4,6):
            move.pieceCaptured.setSquare(None)
            move.pieceCaptured.status = 1
            self.capturedPieces.append(move.pieceCaptured)
            move.toSquare.setPiece(move.piece)
        if type in (3,6):
            move.fromSquare.setPiece(None)
            if move.promoteTo == "q":
                move.toSquare.setPiece(Queen(move.piece.color,move.toSquare,self,True,True))
            if move.promoteTo == "r":
                move.toSquare.setPiece(Rook(move.piece.color,move.toSquare,self,True,True))
            if move.promoteTo == "n":
                move.toSquare.setPiece(Knight(move.piece.color,move.toSquare,self,True,True))
            if move.promoteTo == "b":
                move.toSquare.setPiece(Bishop(move.piece.color,move.toSquare,self,True,True))
            move.pawnPromoted = move.piece
            # A promoted pawn counts as a captured piece for the opponent
            self.capturedPieces.append(move.pawnPromoted)
            move.pawnPromoted.status = 1
        if type == 4:
            self.getSquare(move.toSquare.x, move.fromSquare.y).setPiece(None)
        if type in (0,1,4):
            move.fromSquare.setPiece(None)
            move.piece.setSquare(move.toSquare)
            move.toSquare.setPiece(move.piece)
        # If this move is a pawn moving two squares forward, add it to the list
        if type == 0 and move.piece.type == "p" and abs(move.toSquare.y-move.fromSquare.y) == 2:
            self.whichPawnMoved2.append(move.piece)
        else:
            self.whichPawnMoved2.append(None)
        move.piece.hasMoved = True
        if update:
            # Generate moves and threats for opposite color
            self.generateAllValidMovesAndThreats(True, "white" if move.piece.color == "black" else "black")
            # Generate valid moves for current color to determine if the king is in check
            self.generateAllValidMovesAndThreats(True, move.piece.color)
            self.updateWhichKingInCheck()
            # If opposite king in check, updates checksKing variable of Move object
            if self.whichKingInCheck != None:
                move.setChecksKing(True)
                move.notation += "+"
        return
    
    # Resets all of the variables updated by makeMove()
    def undoMove(self, move):
        if move.type in (0,1,4):
            move.fromSquare.setPiece(move.piece)
            move.piece.setSquare(move.fromSquare)
            move.toSquare.setPiece(None)
        if move.type in (3,6):
            move.fromSquare.setPiece(move.pawnPromoted)
            move.toSquare.setPiece(None)
            self.capturedPieces.remove(move.pawnPromoted)
            move.pawnPromoted.setStatus(0)
            move.pawnPromoted.setSquare(move.fromSquare)
        if move.type in (1,6):
            move.pieceCaptured.setSquare(move.toSquare)
            move.pieceCaptured.setStatus(0)
            self.capturedPieces.remove(move.pieceCaptured)
            move.toSquare.setPiece(move.pieceCaptured)
        if move.type == 4:
            move.pieceCaptured.setSquare(self.getSquare(move.toSquare.x,move.fromSquare.y))
            self.getSquare(move.toSquare.x,move.fromSquare.y).setPiece(move.pieceCaptured)
            move.pieceCaptured.setStatus(0)
            self.capturedPieces.remove(move.pieceCaptured)
        if move.type == 2:
            # The king goes back to the e-file
            move.piece.setSquare(self.getSquare(4, move.toSquare.y))
            self.getSquare(4,move.toSquare.y).setPiece(move.piece)
            move.toSquare.setPiece(None)
            # Moves rook back depending on castling side
            if move.toSquare.x == 2:
                rook = self.getSquare(3,move.toSquare.y).piece
                rook.square.setPiece(None)
                rook.setSquare(self.getSquare(0,move.toSquare.y))
                self.getSquare(0,move.toSquare.y).setPiece(rook)
            else:
                rook = self.getSquare(5,move.toSquare.y).piece
                rook.square.setPiece(None)
                rook.setSquare(self.getSquare(7,move.toSquare.y))
                self.getSquare(7,move.toSquare.y).setPiece(rook)
        self.whichPawnMoved2.pop()
        # If this piece was just moved for the first time, revert hasMoved to False
        if move.isFirstMove:
            move.piece.hasMoved = False
        return

class Square:
    def __init__(self, coordinates=None, piece=None, board=None):
        self.piece = piece
        if piece != None:
            self.pieceColor = piece.color
        else: 
            self.pieceColor = None
        self.coordinates = coordinates
        self.board = board
        # x and y variables for convenience
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]
        # Square's coordinates in notation for convenience
        self.notation = self.getCoordinateNotation()
        return
    def setPiece(self, p):
        self.piece = p
        if self.piece != None:
            self.pieceColor = self.piece.color
        else:
            self.pieceColor = None
        return
    # Returns square coordinates in standard format
    def getCoordinateNotation(self):
        temp = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
        file = temp[self.x]
        rank = str(self.y + 1)
        return file + rank
    # Returns the letter corresponding to this square's file
    def getFile(self):
        return self.notation[0]
    def getRank(self):
        return str(self.y + 1)
# Move types: 0=normal move, 1=capture, 2=castling, 3=promotion, 4=en passant, 5=threat, 6=promotion AND capture
class Move:
    def __init__(self, pieceMoved=None, fromSquare=None, toSquare=None, moveType=None, promoteTo=None):
        self.piece = pieceMoved
        self.fromSquare = fromSquare
        self.toSquare = toSquare
        self.type = moveType
        self.checksKing = False
        self.leavesKingInCheck = False
        self.notation = None
        self.color = self.piece.color
        self.board = self.piece.board
        self.game = self.board.game
        self.promoteTo = promoteTo

        # The pawn which leaves the board when it promotes
        self.pawnPromoted = None
        if moveType in (1,6):
            self.pieceCaptured = toSquare.piece
        if moveType == 4:
            self.pieceCaptured = self.board.getSquare(toSquare.x,fromSquare.y).piece
        if moveType == 0:
            self.pieceCaptured = None
        if moveType == 3:
            if self.toSquare.piece != None:
                self.pieceCaptured = toSquare.piece
        self.isFirstMove = True if self.piece.hasMoved == False else False
    
    def getChecksKing(self):
        return self.checksKing
    
    def setChecksKing(self, c):
        self.checksKing = c
        return
    
    # If update is False, does not run updateLeavesKingInCheck()
    def getLeavesKingInCheck(self, update=True):
        if update:
            self.updateLeavesKingInCheck()
        return self.leavesKingInCheck
    
    def setPiece(self, p):
        self.piece = p
        return

    # Updates notation to account for piece type, whether the move is a capture, and disambiguation
    # Does NOT account for check or checkmate, this must be done after the move is made
    def updateNotation(self):
        if self.type == 2:
            if self.toSquare.x == 2:
                self.notation = "O-O-O"
            else:
                self.notation = "O-O"
            return self.notation
        string = ""
        if self.type in (0,1,3,4,6):
            pieceType = self.piece.type
            if pieceType != "p":
                string += pieceType.upper()
            if self.type in (1,4,6):
                if pieceType == "p":
                    string += self.piece.square.getFile()
                string += "x"
        # Checks for pieces (except pawns) of the same color and type that can also move to the target
        # square, and updates notation accordingly if they can (also returns notation)
        if self.piece.type != "p":
                for piece in self.board.getAllActivePieces(self.color):
                    if piece != self.piece and piece.type == self.piece.type:
                        for move in piece.validMoves:
                            if move.toSquare == self.toSquare:
                                if piece.square.getFile() == self.piece.square.getFile():
                                    string += self.piece.square.getRank()
                                else:
                                    string += self.piece.square.getFile()
        string += self.toSquare.notation
        if self.type in (3,6) and self.promoteTo != None:
            string += "=" + self.promoteTo.upper()
        self.notation = string
        return self.notation
        
    # After this move is made, checks which enemy pieces previously threatened the square that
    # the king is currently on; then regenerates their moves to see if they still threaten it
    # Updates leavesKingInCheck accordingly

    # Works in a similar way to getWhichKingInCheck(), but is significantly more efficient

    def updateLeavesKingInCheck(self):
        oppositeColor = "white" if self.color == "black" else "black"
        threateningPieces = []
        self.board.makeMove(self)
        kingSquare = self.board.getKing(self.color).square
        for move in self.board.getAllThreatenedMoves(oppositeColor):
            if move.toSquare == kingSquare:
                threateningPieces.append(move.piece)
        for piece in threateningPieces:
            piece.generateValidMovesAndThreats(True)
            for move in piece.validMoves:
                if move.toSquare == kingSquare:
                    self.leavesKingInCheck = True
        self.board.undoMove(self)
        return
    

class Piece:
    def __init__(self, color=None, square=None, board=None, status=None, hasMoved=False, promoted=False):
        self.color = color
        self.square = square
        self.x = self.square.x
        self.y = self.square.y
        self.board = board
        self.validMoves = []
        self.threatenedMoves = []
        self.type = ""
        self.hasMoved = hasMoved
        self.promoted = promoted
        # 0 when on the board, 1 when captured
        self.status = 0 if status == None else status
        return
    # Returns only the coordinates that can be moved to
    def getValidMoveCoordinates(self):
        return [i.toSquare.coordinates for i in self.validMoves]
    def getThreatenedSquareCoordinates(self):
        return [i.toSquare.coordinates for i in self.threatenedMoves]
    def setSquare(self, s):
        self.square = s
        if s != None:
            self.x = self.square.x
            self.y = self.square.y
        return
    def setStatus(self, s):
        self.status = s
        if s == 1:
            self.square = None
        return
    
class Pawn(Piece):
    def __init__(self, color=None, square=None, board=None, hasMoved=False):
        super().__init__(color, square, board, hasMoved)
        self.type = "p"
        # 0 if pawn hasn't been moved, 1 if it just moved and en passant is possible,
        # and 2 if it has moved and en passant is not possible
    
    # Updates valid moves and threatened squares for this piece
    # Prevents recursion (updateLeavesKingInCheck() calls this function) by using repeat parameter
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.square
        self.validMoves = []
        self.threatenedMoves = []
        # Determines which way pawn is moving
        if self.color == "white":
            inc = 1
        else:
            inc = -1
        if board.getSquare(self.x, self.y+inc).piece == None:
            if self.y+inc in (0,7):
                # Adds 4 different moves for each possible promoted piece
                for type in ("q","r","n","b"):
                    self.validMoves.append(Move(self,square,board.getSquare(self.x,self.y+inc),3,type))
            else:
                self.validMoves.append(Move(self, square, board.getSquare(self.x, self.y+inc), 0))
                if board.getSquare(self.x, self.y+2*inc).piece == None and not self.hasMoved:
                    self.validMoves.append(Move(self, square, board.getSquare(self.x, self.y+2*inc), 0))
        if self.x!=0:
            current = board.getSquare(self.x-1,self.y+inc)
            self.threatenedMoves.append(Move(self, square, current, 5))
            if current.pieceColor not in (None,self.color):
                if self.y+inc in (0,7):
                    for type in ("q","r","n","b"):
                        self.validMoves.append(Move(self,square,current,6,type))
                else:
                    self.validMoves.append(Move(self,square,current,1))
        if self.x!=7:
            current = board.getSquare(self.x+1,self.y+inc)
            self.threatenedMoves.append(Move(self, square, current, 5))
            if current.pieceColor not in (None,self.color):
                if current.y in (0,7):
                    for type in ("q","r","n","b"):
                        self.validMoves.append(Move(self,square,current,6,type))
                else:
                    self.validMoves.append(Move(self,square,current,1))
        # If an enemy pawn just moved 2 squares and this pawn is next to it,
        # add en passant as a valid move
        temp = self.board.whichPawnMoved2[-1]
        if temp != None:
            if temp.color != self.color:
                if self in temp.getAdjacentEnemyPawns():
                    targetSquare = board.getSquare(temp.x, temp.y+1) if self.color == "white" else board.getSquare(temp.x, temp.y-1)
                    self.validMoves.append(Move(self,square,targetSquare,4))

        if not repeat:
            temp2 = []
            for move in self.validMoves:
                if not move.getLeavesKingInCheck():
                    temp2.append(move)
            self.validMoves = temp2
        return
    
    # Returns a list of enemy pawns that are next to this pawn; this method should be used
    # to update which pawns can capture en passant
    def getAdjacentEnemyPawns(self):
        board = self.board
        result = []
        if self.x != 0:
            target = board.getSquare(self.x-1,self.y)
            if target.pieceColor not in (None, self.color):
                if target.piece.type == "p":
                    result += [target.piece]
        if self.x != 7:
            target = board.getSquare(self.x+1,self.y)
            if target.pieceColor not in (None, self.color):
                if target.piece.type == "p":
                    result += [target.piece]
        return result

class Rook(Piece):
    def __init__(self, color=None, square=None, board=None, hasMoved=False, promoted=False):
        super().__init__(color, square, board, hasMoved, promoted)
        self.type = "r"
        return
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.square
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
                    if current.pieceColor == None:
                        self.validMoves.append(Move(self,square,current,0))
                    elif current.pieceColor != self.color:
                        blocked = True
                        self.validMoves.append(Move(self,square,current,1))
                    else:
                        blocked = True
                inc += 1

        if not repeat:
            temp = []
            for move in self.validMoves:
                if not move.getLeavesKingInCheck():
                    temp.append(move)
            self.validMoves = temp
        return

class Knight(Piece):
    def __init__(self, color=None, square=None, board=None, hasMoved=False, promoted=False):
        super().__init__(color, square, board, hasMoved, promoted)
        self.type = "n"
        return
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.square
        self.validMoves = []
        self.threatenedMoves = []
        self.potentialCoordinates = [(self.x+1,self.y+2),(self.x-1,self.y+2),(self.x+2,self.y+1),(self.x-2,self.y+1),(self.x+2,self.y-1),(self.x-2,self.y-1),(self.x+1,self.y-2),(self.x-1,self.y-2)]
        self.possibleSquares = [board.getSquare(i,j) for (i,j) in self.potentialCoordinates if -1<i<8 and -1<j<8]
        for i in self.possibleSquares:
            self.threatenedMoves.append(Move(self, square, i, 5))
            if i.piece == None:
                self.validMoves.append(Move(self, square, i, 0))
            elif i.pieceColor != self.color:
                self.validMoves.append(Move(self, square, i, 1))

        if not repeat:
            temp = []
            for move in self.validMoves:
                if not move.getLeavesKingInCheck():
                    temp.append(move)
            self.validMoves = temp
        return

class Bishop(Piece):
    def __init__(self, color=None, square=None, board=None, hasMoved=False, promoted=False):
        super().__init__(color, square, board, hasMoved, promoted)
        self.type = "b"
        return 
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.square
        self.validMoves = []
        self.threatenedMoves = []
        for i, j in {(1,1),(1,-1),(-1,1),(-1,-1)}:
            blocked = False
            inc = 1
            while 0<=self.x+i*inc<=7 and 0<=self.y+j*inc<=7:
                current = board.getSquare(self.x+i*inc,self.y+j*inc)
                self.threatenedMoves.append(Move(self, square, current, 5))
                if not blocked:
                    if current.pieceColor == None:
                        self.validMoves.append(Move(self,square,current,0))
                    elif current.pieceColor != self.color:
                        blocked = True
                        self.validMoves.append(Move(self,square,current,1))
                    else:
                        blocked = True
                inc += 1

        if not repeat:
            temp = []
            for move in self.validMoves:
                if not move.getLeavesKingInCheck():
                    temp.append(move)
            self.validMoves = temp
        return

class Queen(Piece):
    def __init__(self, color=None, square=None, board=None, hasMoved=False, promoted=False):
        super().__init__(color, square, board, hasMoved, promoted)
        self.type = "q"
        # Hidden bishop and rook objects used for generateValidMovesAndThreats
        self.bishop = Bishop(self.color,self.square,self.board)
        self.rook = Rook(self.color,self.square,self.board)
        return
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.square
        self.validMoves = []
        self.threatenedMoves = []
        self.bishop.setSquare(square)
        self.rook.setSquare(square)
        self.bishop.generateValidMovesAndThreats(repeat)
        self.rook.generateValidMovesAndThreats(repeat)
        for move in self.bishop.validMoves + self.rook.validMoves:
            move.setPiece(self)
            self.validMoves.append(move)
        for move in self.bishop.threatenedMoves + self.rook.threatenedMoves:
            move.setPiece(self)
            self.threatenedMoves.append(move)

        if not repeat:
            temp = []
            for move in self.validMoves:
                if not move.getLeavesKingInCheck():
                    temp.append(move)
            self.validMoves = temp
        return

class King(Piece):
    def __init__(self, color=None, square=None, board=None, hasMoved=False):
        super().__init__(color, square, board, hasMoved)
        self.type = "k"
        return
    
    def generateValidMovesAndThreats(self, repeat=False):
        board = self.board
        square = self.square
        self.validMoves = []
        self.threatenedMoves = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                current = board.getSquare(self.x+i,self.y+j)
                if current == None:
                    break
                self.threatenedMoves.append(Move(self, square, current, 5))
                if current.piece == None:
                    self.validMoves.append(Move(self,square,current,0))
                elif current.pieceColor != self.color:
                    self.validMoves.append(Move(self,square,current,1))
        # Castling logic; adds castling as a valid move if the king and rook haven't moved,
        # the two adjacent squares are empty and not under attack, and the king isn't in check
        if self.hasMoved == False and board.whichKingInCheck != self.color:
            # Kingside castling
            target = board.getSquare(7,self.y)
            if target.piece != None and target.piece.type == "r" and target.piece.hasMoved == False:
                targetA = board.getSquare(5,self.y)
                targetB = board.getSquare(6,self.y)
                if targetA.piece == None and targetB.piece == None:
                    # If moving the king one square in the same direction would leave the 
                    # king in check, castling is illegal
                    moveA = Move(self, self.square, targetA, 0)
                    if not moveA.getLeavesKingInCheck(update=True):
                        self.validMoves.append(Move(self,square,targetB,2))
            # Queenside castling
            target = board.getSquare(0,self.y)
            if target.piece != None and target.piece.type == "r" and target.piece.hasMoved == False:
                targetA = board.getSquare(3,self.y)
                targetB = board.getSquare(2,self.y)
                if targetA.piece == None and targetB.piece == None:
                    moveA = Move(self, self.square, targetA, 0)
                    moveA.updateLeavesKingInCheck()
                    if not moveA.leavesKingInCheck:
                        self.validMoves.append(Move(self,square,targetB,2))  

        if not repeat:
            temp = []
            for move in self.validMoves:
                if not move.getLeavesKingInCheck():
                    temp.append(move)
            self.validMoves = temp
        return