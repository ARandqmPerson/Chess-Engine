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