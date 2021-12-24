from dataclasses import dataclass
from random import randint
# Mancala

STARTING_STONES = 4
BOARD_LEN = 14
SIDE_LEN = BOARD_LEN//2 - 1
PLAYER1_CAPTURE_PIT = BOARD_LEN//2
PLAYER2_CAPTURE_PIT = 0
PLAYER1 = False
PLAYER2 = True
CAPTURE_MAP = [None] + [i + BOARD_LEN//2 + 1 for i in range(SIDE_LEN)] +\
			  [None] + [i + 1 for i in range(SIDE_LEN)]

@dataclass
class Board:
	board = [0] + [STARTING_STONES] * SIDE_LEN +\
			[0] + [STARTING_STONES] * SIDE_LEN

	turn = PLAYER1
	
	def __str__(self):
		s1 = self.board[:len(self.board)//2]
		s2 = self.board[len(self.board)//2:]
		out = ""
		out += f"P1: {s2[0]} {s1[1:]} \n"
		out += f"P2: {s1[0]} {s2[1:]} \n"
		out += f"Turn: {'Player 1' if self.turn == PLAYER1 else 'Player 2'}"
		return out
	live = lambda self : sum(self.board[1:len(self.board)//2]) and sum(self.board[1+len(self.board)//2:])


def move(cur : Board, pit : int):
	player, board = cur.turn, cur.board
	if player: pit += 7
	
	stones = board[pit]
	if not stones: 
		print(f"Invalid move: {pit} no stones in pit")
		return
	board[pit] = 0
	offset = 1
	
	for i in range(pit, pit + stones):
		if player == PLAYER1 and (i + offset) % BOARD_LEN == PLAYER2_CAPTURE_PIT:
			offset += 1
		elif player == PLAYER2 and (i + offset) % BOARD_LEN == PLAYER1_CAPTURE_PIT:
			offset += 1
		board[(i + offset) % BOARD_LEN] += 1
	lastPit = (i + offset) % BOARD_LEN
	
	# Bonus turns
	if player == PLAYER1 and lastPit == PLAYER1_CAPTURE_PIT:
		cur.turn = not cur.turn
	if player == PLAYER2 and lastPit == PLAYER2_CAPTURE_PIT:
		cur.turn = not cur.turn
	cur.turn = not cur.turn
	
	# Captures
	if player == PLAYER1 and lastPit <= SIDE_LEN and board[lastPit] == 1:
		capturedPits = board[CAPTURE_MAP[lastPit]]
		board[CAPTURE_MAP[lastPit]] = 0
		board[PLAYER1_CAPTURE_PIT] += capturedPits
	if player == PLAYER2 and lastPit > SIDE_LEN and board[lastPit] == 1:
		capturedPits = board[CAPTURE_MAP[lastPit]]
		board[CAPTURE_MAP[lastPit]] = 0
		board[PLAYER2_CAPTURE_PIT] += capturedPits
	assert cur.board == board
		
if __name__ == "__main__":
	b1 = Board()
	while b1.live():
		if b1.turn == PLAYER1:
			m = int(input())
		else:
			m = randint(1, 6)
		move(b1, m)
		print(b1)