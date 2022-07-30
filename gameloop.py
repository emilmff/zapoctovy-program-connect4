from socketserver import DatagramRequestHandler
from board import Board
from minimax import Minimax
from math import inf,floor
from copy import deepcopy
import pygame
import sys
import random

SQUARESIZE = 85
RADIUS = SQUARESIZE//2-3

BROWN = (90, 30, 5)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
ORANGE = (200, 121, 0)
BLUE = (25, 25, 112)
RED = (255,0,0)
AQUA = (127, 255, 212)
GREY = (155, 155, 155)


def draw_text(text, font, color, surface, x, y):
	"""Displays text on a pygame screen
	:param text: A string
	:type param: string 
	:param font: font and size 
	:type font: pygame.font.Font
	:param color: color
	:type color: (int,int,int)
	:param surface: the screen we are drawing on
	:type surface: pygame.Surface
	:param x: x coordinate for location
	:type x: int
	:param y: y coordinate for location
	:type y: int 
	"""
	textobj = font.render(text, 1, color)
	text_rectangle = textobj.get_rect()
	text_rectangle.topleft = (x, y)
	surface.blit(textobj, text_rectangle)

class Human_player:

	def __init__(self):
		pass
	
	def get_move(self,board,screen):
		"""Takes players input through the mouse, shows the player where they are dropping the piece
		:param board: the board the player is making a play on
		:type board: Board
		:param screen: the screen the player plays on
		:type screen: pygame.Surface
		:rtype: int
		:return: the move the player is making
		"""
		colors = {1:CYAN,-1:BROWN}
		color = colors[board.turn]
		col = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, ORANGE, (0,0, board.cols*SQUARESIZE, SQUARESIZE))
				posx = event.pos[0]
				if posx < board.cols*SQUARESIZE -RADIUS:
					pygame.draw.circle(screen, color, (posx, int(SQUARESIZE/2)), RADIUS)
				else:
					pygame.draw.circle(screen, color, (board.cols*SQUARESIZE -RADIUS, int(SQUARESIZE/2)), RADIUS)
			pygame.display.update()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK, (0,0, board.cols*SQUARESIZE , SQUARESIZE))
				posx = event.pos[0]
				col = int(posx//SQUARESIZE)
				if col in board.possible_moves():
					return col
		
class Random_player:
	def __init__(self):
		pass

	def get_move(self,board,screen):
		"""Makes a random move, same parameters as the other players to fit the pattern and return 
		"""
		moves = board.possible_moves()
		return random.choice(moves)

class Minimax_player:

	def __init__(self,depth):
		"""Gets depth for minimax
		:param depth: depth of minimax
		:type depth: int
		"""
		self.depth = depth
		

	def get_move(self,board,screen):
		"""Calls on minimax to make a move, same params and return as Human_player
		"""
		m = Minimax(deepcopy(board))
		val, turn = m.minimax(self.depth,-inf,inf,True,None,None)
		return turn

class Game_Loop:

	def __init__(self, player1,player2,start = 1,rows=6,cols=7,wins = 4):
		"""Creates a board and a screen
		:param player1: first player
		:type player1: Human_player, Random_player or Minimax_player
		:param player2: second player
		:type player2: Human_player, Random_player or Minimax_player
		:param start: what color starts
		:type start: int
		:param rows: rows of the board thats played on
		:type rows: int
		:param rows: columns of the board thats played on
		:type rows: int
		:param wins: how many in a row win
		:type wins: int
		"""
		self.board = Board(rows,cols,1,wins)
		self.player1 = player1
		self.player2 = player2
		if start == 1:
			self.call = {1:self.player1,-1:self.player2}
		else:
			self.call = {-1:self.player1,1:self.player2}
		main = max(self.board.rows,self.board.cols)
		width = main*SQUARESIZE	
		self.height = (main+1)*SQUARESIZE
		screen_size = (width, self.height)
		self.screen = pygame.display.set_mode(screen_size)

	
	def draw_board(self):
		"""Draws the board from the underlying matrix of the board
		"""
		for c in range(self.board.rows):
			for r in range(self.board.cols):
				pygame.draw.rect(self.screen, BLUE, (r*SQUARESIZE, c*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
				pygame.draw.circle(self.screen, BLACK, (int(r*SQUARESIZE+SQUARESIZE/2), int(c*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
		for c in range(self.board.rows):
			for r in range(self.board.cols):		
				if self.board.board[c][r] == 1:
					pygame.draw.circle(self.screen, CYAN, ( int((r)*SQUARESIZE+SQUARESIZE/2),int((c+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
				elif self.board.board[c][r] == -1: 
					pygame.draw.circle(self.screen, BROWN, (int(r*SQUARESIZE+SQUARESIZE/2), int((c+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
				else:
					pygame.draw.circle(self.screen, WHITE, (int(r*SQUARESIZE+SQUARESIZE/2), int((c+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
		if self.board.rows>self.board.cols:
			pygame.draw.rect(self.screen,RED,(self.board.cols*SQUARESIZE,0,SQUARESIZE*(self.board.rows-self.board.cols),SQUARESIZE*(self.board.rows+1)))
		elif self.board.rows<self.board.cols:
			pygame.draw.rect(self.screen,RED,(0,(self.board.rows+1)*SQUARESIZE,SQUARESIZE*(self.board.cols+1),SQUARESIZE*(self.board.cols-self.board.rows)))
		pygame.display.update()

	def loop(self):
		"""Puts it all together in a while loop, calls on players to make moves, calls the self.draw_board function, when the game ends, displays who won and creates a button to continue
		"""
		end = False
		self.draw_board()
		tie = False
		while end != True:
			turn = self.board.turn
			if self.board.possible_moves():		
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
				tie = True
			if end == True:
				pygame.draw.rect(self.screen, BLACK, (0,0, self.board.cols*SQUARESIZE , SQUARESIZE))
				click = False
				if tie:
					draw_text("TIE",pygame.font.SysFont("arial", 75),WHITE,self.screen,0,0)
				elif self.call[turn] == self.player1:
					draw_text("YOU WON",pygame.font.SysFont("arial", 75),WHITE,self.screen,0,0)
				else:
					draw_text("YOU LOST",pygame.font.SysFont("arial", 75),WHITE,self.screen,0,0)
				
				continue_button = pygame.Rect(300,0,250,SQUARESIZE)
				pygame.draw.rect(self.screen,WHITE,continue_button)
				draw_text("CONTINUE",pygame.font.SysFont("arial", 60),BLACK,self.screen,300,0)

				while True:
					mx,my = pygame.mouse.get_pos()
					if continue_button.collidepoint(mx,my):
							if click:
								return

					click = False
					for event in pygame.event.get():

						if event.type == pygame.QUIT:
							sys.exit()
						if event.type == pygame.MOUSEBUTTONDOWN:
							if event.button == 1:
								click = True
					pygame.display.update()
		

