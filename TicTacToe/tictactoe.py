# tic tac toe solver


'''	
	board:
		first 9 bits X occupancy
			0 1 2
			3 4 5
			6 7 8
		
		next 9 bits O occupancy
			 9 10 11
			12 13 14
			15 16 17
	
		next bit turn (0 for X, 1 for O) (bit 18)
	Player X goes first
'''


TURN = 1 << 18
FULL = (1 << 9) - 1
ROWS = [0b000000111, 0b000111000, 0b111000000]
COLS = [0b100100100, 0b010010010, 0b001001001]
DIAG = [0b100010001, 0b001010100]
ALL = ROWS + COLS + DIAG

moveCache = {}

# 8 bit operations (less if someone won)
def checkWinner(board):
	if any(board & won == won or ((board >> 9) & won == won) for won in ALL): 
		return 0 if ((board & TURN) >> 18) else 1
	return None

def p(board):
	for i in range(9):
		if board & (1 << i):
			print("X", end="\t")
		elif board & (1 << (i + 9)):
			print("O", end="\t")
		else:
			print(" ", end="\t")
		if i % 3 == 2: print()
	print(f"Turn: {'O' if TURN & board else 'X'}\n")

# generates next move based on board state
def generateNextMove(board):
	occupied = (board | (board >> 9)) & FULL
	moves = []
	for i in range(9):
		if (1 << i) & occupied == 0:
			move = (1 << (i + 9)) if TURN & board else (1 << i)
			moves += [(board | move) ^ TURN]
	
	moveCache[board] = (moves[0], optimalMove(moves[0])[1])
	if bool(moveCache[board][1]) == bool(TURN & board):
		return moveCache[board]
	
	for move in moves[1:]:
		result = optimalMove(move)[1]
		if result == None:
			moveCache[board] = (move, result)
		if bool(TURN & board) == bool(result):
			moveCache[board] = (move, result)
			break

# returns optimal move and result of move
def optimalMove(board):
	if board in moveCache:
		return moveCache[board]
	
	winner = checkWinner(board)
	if winner != None:
		moveCache[board] = (board, winner)
	elif (board | (board >> 9)) & FULL == FULL:
		moveCache[board] =  (board, None)
	else:
		generateNextMove(board)
	return moveCache[board]
	
# valid moves 0-8
def playMove(board : int, move : int):
	move = (1 << move)
	if board & TURN: move <<= 9
	board |= move
	return board ^ TURN

if __name__ == "__main__":
	board = 0
	human = 0
	for i in range(9):
		if i % 2 == human:
			move = int(input())
			board = playMove(board, move)
		else:
			board = optimalMove(board)[0]
		p(board)
