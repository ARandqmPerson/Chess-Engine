from chess import *

game = Game()
print("""
Commands:
history - See list of previously played moves
moves - See list of moves you can play
undo - Undo the previously played move
board - View the board and pieces
""")

gameInProgress = True
while gameInProgress:
    string = input("("+game.whoseMove.capitalize()+") Input your move: ")
    if string == "history":
        game.displayMoveList()
    elif string == "moves":
        game.board.displayValidMoves()
    elif string == "undo":
        print("Took back the move " + game.moveList[-1].notation + ".")
        game.undoLastMove()
    elif string == "board":
        game.board.displayBoard()
    else:
        # Allows lowercase, so an input like "nf3" or "o-o" is valid
        if "o-o" in string:
                string = string.upper()
        if not game.makeMove(string) and not game.makeMove(string.capitalize()):
            print("Invalid move, try again;")
        else:
            if game.gameOver != 0:
                gameInProgress = False
                if game.gameOver == 1:
                    print(("White" if game.whoseMove=="black" else "Black")+" wins by checkmate!")
                elif game.gameOver == 2:
                    print("Draw by stalemate!")
                elif game.gameOver == 3:
                    print("Draw by threefold repetition!")
                    str = "The position repeated on moves "
                    for i in range(0,len(game.board.shortFENs)):
                        if game.board.shortFENs[i] == game.board.shortFENs[-1]:
                            str += str(int((i + 1)/2)) + ", "
                    str = str[:-2]
                    print(str)
                elif game.gameOver == 4:
                    print("Draw by 50-move rule!")
                loop = True
                while loop:
                    playAgain = input("Play again? (Y/N): ")
                    if playAgain.upper() == "Y":
                        gameInProgress = True
                        game = Game()
                        loop = False
                    elif playAgain.upper() == "N":
                        loop = False
                    else:
                        print("Invalid input;")