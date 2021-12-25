import pygame
import os
from mancala import *
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mancala")

WHITE = (255, 255, 255)
POT_FONT = pygame.font.SysFont('ariel', 40)
WINNER_FONT = pygame.font.SysFont('ariel', 100)

FPS = 10
HIGHLIGHT_WIDTH, HIGHLIGHT_HEIGHT = 100, 20

PLAYER2_HIGHLIGHT_IMAGE = pygame.image.load(os.path.join('Assets', 'highlight.png'))
PLAYER2_HIGHLIGHT = pygame.transform.scale(PLAYER2_HIGHLIGHT_IMAGE, (HIGHLIGHT_WIDTH, HIGHLIGHT_HEIGHT))

PLAYER1_HIGHLIGHT_IMAGE = pygame.image.load(os.path.join('Assets', 'highlight2.png'))
PLAYER1_HIGHLIGHT = pygame.transform.scale(PLAYER1_HIGHLIGHT_IMAGE, (HIGHLIGHT_WIDTH, HIGHLIGHT_HEIGHT))

BOARD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'board.png')), (WIDTH, HEIGHT))


def draw_window(player1, player2, boa=None):
	WIN.blit(BOARD, (0, 0))
	a = boa.board[1:7]
	b = boa.board[14:7:-1]
	for i in range(6):
		WIN.blit(POT_FONT.render(str(a[i]), 1, WHITE), (180 + 100*i, 260))
		WIN.blit(POT_FONT.render(str(b[i]), 1, WHITE), (180 + 100*i, 160))
	
	WIN.blit(POT_FONT.render(str(boa.board[0]), 1, WHITE), (80, 210))
	WIN.blit(POT_FONT.render(str(boa.board[7]), 1, WHITE), (780, 210))
	
	if boa.turn:
		WIN.blit(POT_FONT.render("Player 2", 1, WHITE), (400, 50))
		WIN.blit(PLAYER2_HIGHLIGHT, (player2.x, player2.y))
	else:
		WIN.blit(POT_FONT.render("Player 1", 1, WHITE), (400, 350))
		WIN.blit(PLAYER1_HIGHLIGHT, (player1.x, player1.y))
	
	pygame.display.update()


def player_handle_movement(keys_pressed, player):
	if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and player.x > 180:
		player.x -= 100
	if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and player.x + player.width < 700:
		player.x += 100

def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
						 2, HEIGHT/2 - draw_text.get_height()/2))
	pygame.display.update()
	pygame.time.delay(5000)


def main():
	b1 = Board()
	player1 = pygame.Rect(140, 330, HIGHLIGHT_WIDTH, HIGHLIGHT_HEIGHT)
	player2 = pygame.Rect(140, 100, HIGHLIGHT_WIDTH, HIGHLIGHT_HEIGHT)
	
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if b1.turn == PLAYER1:
						m = player1.x//100
					else:
						m = 7 - player2.x//100
					move(b1, m)
		

		keys_pressed = pygame.key.get_pressed()
		player_handle_movement(keys_pressed, player1)
		player_handle_movement(keys_pressed, player2)
		
		draw_window(player1, player2, b1)

		if not b1.live():
			draw_winner("p2 wins" if sum(b1.board[:7]) > sum(b1.board[7:]) else "p1 wins")
			exit()
	main()


if __name__ == "__main__":
	main()
