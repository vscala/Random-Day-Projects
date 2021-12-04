BLACK = 0
WHITE = 1

RANK8_MASK = 0x00000000000000ff
RANK7_MASK = 0x000000000000ff00
RANK6_MASK = 0x0000000000ff0000
RANK5_MASK = 0x00000000ff000000
RANK4_MASK = 0x000000ff00000000
RANK3_MASK = 0x0000ff0000000000
RANK2_MASK = 0x00ff000000000000
RANK1_MASK = 0xff00000000000000

FILE1_MASK = 0x8080808080808080
FILE2_MASK = 0x4040404040404040
FILE3_MASK = 0x2020202020202020
FILE4_MASK = 0x1010101010101010
FILE5_MASK = 0x0808080808080808
FILE6_MASK = 0x0404040404040404
FILE7_MASK = 0x0202020202020202
FILE8_MASK = 0x0101010101010101

class Board:
    def __init__(self):
        self.white_king   = 0x1000000000000000
        self.white_queen  = 0x0800000000000000
        self.white_rook   = 0x8100000000000000
        self.white_knight = 0x4200000000000000
        self.white_bishop = 0x2400000000000000
        self.white_pawn   = 0x00ff000000000000

        self.black_king   = 0x0000000000000010
        self.black_queen  = 0x0000000000000008
        self.black_rook   = 0x0000000000000081
        self.black_knight = 0x0000000000000042
        self.black_bishop = 0x0000000000000024
        self.black_pawn   = 0x000000000000ff00

        self.black_occupied = RANK8_MASK | RANK7_MASK
        self.white_occupied = RANK1_MASK | RANK2_MASK
        self.both_occupied = self.black_occupied | self.white_occupied

    def __str__(self):
        out = ""
        for i in range(64):
            if   self.white_king   & (1 << i): out += " K "
            elif self.white_queen  & (1 << i): out += " Q "
            elif self.white_rook   & (1 << i): out += " R "
            elif self.white_knight & (1 << i): out += " N "
            elif self.white_bishop & (1 << i): out += " B "
            elif self.white_pawn   & (1 << i): out += " P "
            
            elif self.black_king   & (1 << i): out += " k "
            elif self.black_queen  & (1 << i): out += " q "
            elif self.black_rook   & (1 << i): out += " r "
            elif self.black_knight & (1 << i): out += " n "
            elif self.black_bishop & (1 << i): out += " b "
            elif self.black_pawn   & (1 << i): out += " p "
            
            else: out += " - "
            
            if i % 8 == 7: out += "\n"
        return out

class Chess:
    def __init__(self):
        self.board = Board()

    # Calculate moves
    def pawnMoves(self, color = BLACK):
        moves = {"left captures" : 0, "right captures" : 0, "forward one" : 0, "forward two" : 0}
        occupied = self.board.both_occupied
        if color == BLACK:
            current_pawns = self.board.black_pawn
            # Move pawns forward one and remove pawns that are blocked
            moves["forward one"] = (current_pawns << 8) & ~occupied
            # Move pawns forward two and remove pawns that are blocked
            moves["forward two"] = ((((current_pawns & RANK7_MASK) << 8) & ~occupied) << 8) & ~occupied
            # Capture left
            moves["left captures"] = ((current_pawns & ~FILE1_MASK) << 7) & self.board.white_occupied
            # Capture right
            moves["right captures"] = ((current_pawns & ~FILE8_MASK) << 9) & self.board.white_occupied

        if color == WHITE:
            current_pawns = self.board.white_pawn
            # Move pawns forward one and remove pawns that are blocked
            moves["forward one"] = current_pawns >> 8
            # Move pawns forward two and remove pawns that are blocked
            moves["forward two"] = ((((current_pawns & RANK2_MASK) >> 8) & ~occupied) >> 8) & ~occupied
            # Capture left
            moves["left captures"] = ((current_pawns & ~FILE8_MASK) >> 9) & self.board.black_occupied
            # Capture right
            moves["right captures"] = ((current_pawns & ~FILE1_MASK) >> 7) & self.board.black_occupied

        return moves
    
    # prints a long as an 8x8 board
    def printMoves(moves):
        flat = bin(moves)[2:].zfill(64)
        print(*(flat[i*8:i*8+8] for i in range(8)), sep = "\n")




if __name__ == "__main__":
    game = Chess()
    print(game.board)
    pawnMoves = game.pawnMoves(WHITE)
    for move in pawnMoves:
        print(move)
        Chess.printMoves(pawnMoves[move])