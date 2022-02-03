# TicTacToe Solver
Used DP for computating the best move and a bitboard to hold the current state of the boad.

## TODO
bitboard rotations to prune game tree

1 2 3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;7 4 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;9 8 7&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3 6 9  
4 5 6 == 8 5 2 == 6 5 4 == 2 5 8  
7 8 9&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;9 6 3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3 2 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 4 7

(and diagonal/horizontal/vertical flips)
