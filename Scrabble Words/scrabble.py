from collections import defaultdict

# Read words
with open('words.txt') as f:
    words = f.readlines()

# Map letters to possible words
wordmap = defaultdict(list)
for word in words:
	word = word[:-1]
	sword = "".join(sorted(word))
	wordmap[sword].append(word)

# Find words made from given letters
def find(letters):
	return wordmap["".join(sorted(letters.upper()))]

# Main input loop
ALPH = 'abcdefghijklmnopqrstuvwxyz'
while True:
	letters = input()
	print("Possible words: ", find(letters))
	print("Words +1 letter:", list(find(letters+a) for a in ALPH))
	print("Words -1 letter:", list(find(letters[:i] + letters[i+1:]) for i in range(len(letters))))