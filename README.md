# Summary

This program, specifically chess.py, allows two players to play a game of chess. It keeps track of all moves played and prevents players from making illegal moves.

It is *not* an engine like Stockfish that calculates the best moves. It only calculates which moves are legal and monitors the game state.

### Why I wrote it

I began this project because I wanted to gain experience with Python and software engineering. As I've gone along, I've learned a lot about the basics of python classes, objects, data structures, etc., and I've worked on best practices like documentation and consistent commits with good commit messages.

When I first started, I did not realize how logistically complex the rules of chess are. There are so many edge cases and calculations that need to be made just to determine a legal move. However, I'm actually quite glad it has provided such a challenge.

### A note on AI:

**All of the code in this project was written myself. I never asked an AI model for feedback on my code, nor how I should write and debug the code or structure the program.**

I understand that this program would be trivial for an AI chatbot, but I didn't start this project just to have a finished product.

# How it works

(This section is unfinished)

## Explanation of threatened moves:

When a move is made, the list of all valid moves is updated (so the next move can be checked for validity). Updating this list requires updating valid moves for each piece. Testing for move validity includes testing whether each move leaves the king in check.

This could be done by regenerating all valid moves (but not using check detection so there isn't recursion), but that would take a lot of processing as it would be done 20-50 times for EVERY move (see below for an example).

Instead, I've included a "threatened moves" feature. Here's how it works:
In chess, it's illegal to make a move that leaves you in check. This means that your king cannot be left on a square that an enemy piece can also move to. There are two situations where your move could allow your opponent's pieces to "see" the square your king is currently on: if you move your king to that square, or if you move a piece that was "pinned" (blocking the enemy piece's line of sight).

Therefore, threatened moves include moves that *could* be played after your move is played. If one of these moves would land on the same square that your king is on, that means you would be in check, so your move would be invalid.

So after a move is played, threatened moves are generated. After that, all potential moves will be checked for validity; if they leave the king on a square that is targeted by one of the moves in the list, then ONLY the pieces which "target" that square will have their moves regenerated. Threatened moves ignore pieces that block their line of sight, because that piece may be moved.

### Here's a visualization of what would happen without threatened moves:

Move is made --> 16 pieces have their valid moves generated, 50 moves in total --> Each move is tested for leaving the king in check --> For each of the 50 moves, another 16 pieces have their moves generated, meaning another 50 moves are calculated. In total, moves are generated **800 times.**

But with threatened moves, only one or two pieces have their moves generated, if any. Moves would only be generated **80 times.**

(This is only an example, and the numbers will obviously widely vary.)