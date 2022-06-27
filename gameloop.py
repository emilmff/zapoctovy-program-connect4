from board import Board
from minimax import Minimax
from math import inf,floor
from copy import deepcopy
import pygame
import sys

SQUARESIZE = 85
RADIUS = SQUARESIZE//2-3

BROWN_COLOR = (90, 30, 5)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
ORANGE = (200, 121, 0)
BLUE = (25, 25, 112)
RED = (255,0,0)

def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	text_rectangle = textobj.get_rect()
	text_rectangle.topleft = (x, y)
	surface.blit(textobj, text_rectangle)

class Human:

	def __init__(self):
		pass
	
	def get_move(self,board,screen):
		col = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, ORANGE, (0,0, board.cols*SQUARESIZE, SQUARESIZE))
				posx = event.pos[0]
				if posx < board.cols*SQUARESIZE -RADIUS:
					pygame.draw.circle(screen, CYAN, (posx, int(SQUARESIZE/2)), RADIUS)
				else:
					pygame.draw.circle(screen, CYAN, (board.cols*SQUARESIZE -RADIUS, int(SQUARESIZE/2)), RADIUS)
			pygame.display.update()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK, (0,0, board.cols*SQUARESIZE , SQUARESIZE))
				posx = event.pos[0]
				col = int(posx//SQUARESIZE)
				if col in board.possible_moves():
					return col
		
class minimax_player:

	def __init__(self):
		self.val = 0
		

	def get_move(self,board,screen):
		m = Minimax(deepcopy(board))
		self.val, turn = m.minimax(7,-inf,inf,True,None,None)
		return turn

class Game_Loop:

	def __init__(self, player1,player2):
		self.board = Board()
		self.player1 = player1
		self.player2 = player2
		self.call = {1:self.player1,-1:self.player2}		
		main = max(self.board.rows,self.board.cols)
		width = main*SQUARESIZE	
		self.height = (main+1)*SQUARESIZE
		screen_size = (width, self.height)
		self.screen = pygame.display.set_mode(screen_size)

	
	def draw_board(self):
		for c in range(self.board.rows):
			for r in range(self.board.cols):
				pygame.draw.rect(self.screen, BLUE, (r*SQUARESIZE, c*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
				pygame.draw.circle(self.screen, BLACK, (int(r*SQUARESIZE+SQUARESIZE/2), int(c*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
		for c in range(self.board.rows):
			for r in range(self.board.cols):		
				if self.board.board[c][r] == 1:
					pygame.draw.circle(self.screen, CYAN, ( int((r)*SQUARESIZE+SQUARESIZE/2),int((c+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
				elif self.board.board[c][r] == -1: 
					pygame.draw.circle(self.screen, BROWN_COLOR, (int(r*SQUARESIZE+SQUARESIZE/2), int((c+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
				else:
					pygame.draw.circle(self.screen, WHITE, (int(r*SQUARESIZE+SQUARESIZE/2), int((c+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
		if self.board.rows>self.board.cols:
			pygame.draw.rect(self.screen,RED,(self.board.cols*SQUARESIZE,0,SQUARESIZE*(self.board.rows-self.board.cols),SQUARESIZE*(self.board.rows+1)))
		elif self.board.rows<self.board.cols:
			pygame.draw.rect(self.screen,RED,(0,(self.board.rows+1)*SQUARESIZE,SQUARESIZE*(self.board.cols+1),SQUARESIZE*(self.board.cols-self.board.rows)))
		pygame.display.update()

	def loop(self):
		end = False
		self.draw_board()
		while end != True:
			if self.board.possible_moves():
				turn = self.board.turn
				col = self.call[turn].get_move(self.board,self.screen)
				while col is None:
					col = self.call[turn].get_move(self.board,self.screen)
				row,col = self.board.drop_piece(col,turn)
				end = self.board.check_for_win(row,col,turn)
				self.board.change_turn()
				if self.board.until_flip == 1:
					self.board.flip()
					self.board.until_flip = 2
				else:
					self.board.until_flip -=1
				self.draw_board()
			else:
				end= True
			if end == True:
				pygame.time.wait(6000)
		

h1= Human()
h2 = minimax_player()
game = Game_Loop(h1,h2)
game.loop()
	 
