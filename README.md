Run play_chess.py to play a game using the console.

# Summary

This program allows two players to play a game of chess. It is *not* an engine like Stockfish that calculates the best moves.

### Features

In any legal chess position, all moves that can be legally played by the current side are calculated and stored. Check, checkmate, stalemate, 50-move rule, and threefold repetition are also detected. The amount of moves played, the list of previous moves, and the side whose turn it is are also tracked. A position can be "set up" by importing an FEN, or it can be saved by exporting.

Users can play a game by entering moves in algebraic notation. They can also view previously played moves, get a list of legal moves, see a visual of the board, or undo the last played move. When one player wins or a draw occurs, the game automatically declares the result and allows users to play again.

## Why I wrote it

I began this project because I wanted to gain experience with Python and SE best practices, but also because it's the type of challenge that I find fun. As I've gone along, I've learned a lot about the basics of Python classes, objects, data structures, syntax, etc., and I've used best practices like documentation, testing, detailed commit messages, and making code readable and efficient.

*(Fun fact: the numbers at the end of commit messages represent total hours spent!)*

When I first started, I did not realize how logistically complex the rules of chess are. There are so many edge cases and calculations that need to be made just to determine a legal move. However, I'm actually quite glad it has provided such a challenge.

### A note on AI

**All of the code in this project was written myself. I never asked an AI model for feedback on my code, nor how I should write and debug the code or structure the program.**

# How it works

(*This section doesn't cover everything, but most information can also be found in the comments of chess.py*)

## Structure of chess.py

There are Game, Board, Piece, Move, and Square classes (in approximate order of importance). The Game object stores a Board object; the Board object stores 64 Square objects and two lists of Move objects; Square objects store Piece objects; Piece objects store two lists of Move objects.

References also go the other way: Board has a Game, Moves have a Board, Pieces have a Board and a Square, Squares have a Board, Moves have a Piece and Squares.

### Generating valid moves

The makeMove method of the Game class is the main function, but the most complicated function is generateAllValidMovesAndThreats of the Board class, which I will call gAVM for clarity. gAVM calls generateValidMovesAndThreats (I'll call this gVM) for each piece. gVM calculates all legal moves depending on the current state of the board and the rules for the piece. (This is only an explanation of valid moves, **threatened moves are explained below.**)

For example, when gVM is called on a rook, it looks for all squares with the same x or y coordinates as the rook's, then checks which ones have pieces on them and which ones are blocked, then adds Move objects to a validMoves (vM) list. However, a move that leaves the king in check is illegal, so that is checked first (also explained below). This list is then returned to the Board where gAVM was called. The board has an allValidMoves (aVM) attribute, where the vMs of all pieces are appended.

### Updating notation

Each move, when checked for validity, is passed to the makeMove function of the *Board* class (not Game). This plays the move to test whether it leaves the king in check. However, this also generates the algebraic notation for this move, which is useful for multiple different functions. It makes debugging easier (assuming you're familiar with notation), but most importantly, it lets users input moves with notation.

When the user inputs a move (a string containing the notation representing their intended move), the previously generated aVM is scanned to see if any valid move has notation that matches the user's input. If there isn't one, nothing happens and the user can try again. If there is one, the second part of chess.py starts working.

### Making the move

The makeMove function of Board is called with the intended move passed as a parameter. Depending on the type of move (which is set when the contructor is called), makeMove changes the Square referenced by the Piece to the "target" square and updates the Squares' "piece" attributes accordingly. If the update parameter is True, it will also update whether this move is a check/checkmate/draw and whether it leaves the king in check.

## Check detection

The most challenging restriction is that a move *cannot* be played if it leaves the king of the same color attacked by another piece. My solution is to call Board's makeMove *again* for each valid move.

### Example

Say the player with Black has just moved their rook to e8. gAVM calls on a knight on e2, and move A is the move currently being checked for validity. gVM calls makeMove on move A. Let's say move A would allow the e8 rook to "see" the king on e1, making it illegal. It doesn't matter whether move A is a check, checkmate, stalemate, etc.; all that matters is whether it leaves the king in check, which can only be (easily) determined by playing the move. If it does, it's removed from the validMoves list. This process is repeated for every move that is *otherwise* valid.

### Update parameter

This is where the update parameter comes in. gVM calls makeMove(False), meaning the update does not occur, so things like check and checkmate aren't calculated (side note: that calculation would also cause a recursion error since it requires makeMove). Update is only necessary when the move is being played by the user, and gAVM must be called so move validity can be determined in preparation for the *next* move.

## Threatened moves

When a move is made, the list of all valid moves is updated (so the next move can be checked for validity). Updating this list requires updating valid moves for each piece. Testing for move validity includes testing whether each move leaves the king in check.

This could be done by regenerating all valid moves (not using check detection so there isn't recursion), but that would take a lot of processing as it would be done 20-50 times for EVERY move (see below for an example).

Instead, I've included a "threatened moves" feature. Here's how it works:
In chess, it's illegal to make a move that leaves you in check. This means that your king cannot be left on a square that an enemy piece can also move to. There are two situations where your move could allow your opponent's pieces to "see" the square your king is currently on: if you move your king to that square, or if you move a piece that was "pinned" (blocking the enemy piece's line of sight).

Therefore, threatened moves include moves that *could* be played after your move is played. If one of these moves would land on the same square that your king is on, that means you would be in check, so your move would be invalid.

So after a move is played, threatened moves are generated. After that, all potential moves will be checked for validity; if they leave the king on a square that is targeted by one of the moves in the list, then ONLY the pieces which "target" that square will have their moves regenerated. Threatened moves ignore pieces that block their line of sight, because that piece may be moved.

### Here's a visualization of what would happen without threatened moves:

Move is made --> 16 pieces have their valid moves generated, 50 moves in total --> Each move is tested for leaving the king in check --> For each of the 50 moves, another 16 pieces have their moves generated, meaning another 50 moves are calculated. In total, moves are generated **800 times.**

But with threatened moves, only one or two pieces have their moves generated, if any. Moves would only be generated **80 times.**

(This is only an example, and the numbers will obviously widely vary.)