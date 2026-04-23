from chess import *

game = Game()
print("""
At any time, type "history" to see move history or "list" to see a list of possible moves.
When inputting moves, use standard notation (like "e4" or "Nxe5")
""")

gameInProgress = True
while gameInProgress:
    string = input("("+game.whoseMove.capitalize()+") Input your move: ")
    if string == "history":
        game.displayMoveList()
    elif string == "list":
        game.board.displayValidMoves()
    else:
        if game.makeMove(string)==False:
            print("Invalid move, try again;")
        else:
            if game.gameOver == 1:
                gameInProgress = False
                print(("White" if game.whoseMove=="black" else "Black")+" wins by checkmate!")
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