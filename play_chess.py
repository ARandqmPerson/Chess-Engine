from chess import *

game = Game()
string = input("""
At any time, type "history" to see move history or "list" to see a list of possible moves.
When inputting moves, use standard notation (like "e4" or "Nxe5")
(White) Input your move:      
""")

while True:
    if string == "history":
        game.displayMoveList()
    elif string == "list":
        game.board.displayValidMoves()
    else:
        if game.makeMove(string)==False:
            print("Invalid move")
    string = input("("+game.whoseMove.capitalize()+") Input your move: ")