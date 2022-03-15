# SpellCast

from collections import defaultdict, Counter
from itertools import chain

class WordBoard:
	def setBoard(self, board):
		self.board = board
		self.n = len(board)
		self.m = len(board[0])
		self.totalCount = Counter(chain(*board))
	
	def precheck(self, word):
		wCount = Counter(word)
		for c in wCount:
			if wCount[c] > self.totalCount[c]: return False
		return True
		
	def boardContains(self, word, skips=0) -> bool:
		n, m = self.n, self.m
		if not skips and not self.precheck(word):
			return False
		# TODO precheck with skips
		
		def backtrack(i, j, letters, skips=0):
			if not letters: return True
			if self.board[i][j] != letters[0]: 
				if skips and board[i][j] != '.': skips -= 1
				else: return False
			
			temp, self.board[i][j] = self.board[i][j], "."
			out = False
			if i+1 < n: 
				out = out or backtrack(i+1, j, letters[1:]) 		# +1, 0
				if j+1 < m:
					out = out or backtrack(i+1, j+1, letters[1:]) 	# +1, +1
				if j > 0:
					out = out or backtrack(i+1, j-1, letters[1:])	# +1, -1
			if i > 0: 
				out = out or backtrack(i-1, j, letters[1:]) 		# -1, 0
				if j+1 < m:
					out = out or backtrack(i-1, j+1, letters[1:]) 	# -1, +1
				if j > 0:
					out = out or backtrack(i-1, j-1, letters[1:])	# -1, -1
			if j+1 < m: 
				out = out or backtrack(i, j+1, letters[1:]) 		# 0, +1
			if j > 0: 
				out = out or backtrack(i, j-1, letters[1:])		# 0, -1
			self.board[i][j] = temp
			return out	
	   	
		#Iterate over board
		for i in range(n):
			for j in range(m):
				if board[i][j] == word: return True
				if board[i][j] == word[0]:
					if backtrack(i, j, word):
						return True   

# Read words
with open('words.txt') as f:
	words = [word[:-1] for word in f.readlines()]

# Spellcast letter values / charset
letter_values = [1, 4, 5, 3, 1, 5, 3, 4, 1, 7, 3, 3, 4, 2, 1, 4, 8, 2, 2, 2, 4, 5, 5, 7, 4, 8] 
charset = set('abcdefghijklmnopqrstuvwxyz')

# map words to their values
value = lambda word : sum(letter_values[ord(c.lower()) - ord('a')] for c in word if c.lower() in charset)
word_values = [(value(word), word) for word in words]
word_values.sort(reverse=True)

# Read board and create wordboard
board = [[c.lower() for c in input()] for _ in range(5)]
wb = WordBoard()
wb.setBoard(board)

# Find best word(s)
for value, word in word_values:
	if wb.boardContains(word):
		print(word, value)
		query = input()
		if query != "":
			break

