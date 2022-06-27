from ast import excepthandler
from board import Board
from math import inf
from copy import *
import random

class Minimax:

	def __init__(self, board):
		self.board = board
		self.colors = {True:self.board.turn, False:-self.board.turn}

	
	def eval(self):
		dic ={-3:0,-2:0,-1:0,0:0, 1:0,2:0,3:0}
		dirs = []
		for i in range(self.board.rows):
			for j in range (-1,2):
				dirs.append(self.board.search_direction((i,0),(j,1)))
		
		for i in range(self.board.cols):
			for j in range (-1,2):				
				dirs.append(self.board.search_direction((0,i),(1,j)))
		#print(dirs)
		for dir in dirs:
			chunks = []				
			for i in range(1,(len(dir)//4)+1):
				chunks.append(dir[(i-1)*4:i*4])
			if len(dir)%4 != 0:
				chunks.append(dir[len(dir)-len(dir)%4:])
			#print(chunks)
			for c in chunks:
				dic[c.count(self.colors[True])-c.count(self.colors[False])] +=1				
		score = dic[-3]*-24 + dic[-2]*-9+dic[2]*10+dic[3]*25
		#print(score)
		return score

	def minimax(self, depth, alpha, beta, maximizing,prev_row,prev_col):

		if (prev_row is not None) and (prev_col is not None):
			if self.board.until_flip == 2:
				if self.board.check_for_win(prev_col,prev_row,-self.colors[maximizing]):
					if maximizing:
						return -inf,None
					else:
						return inf,None
			else:
				if self.board.check_for_win(prev_row,prev_col,-self.colors[maximizing]):
					if maximizing:
						return -inf,None
					else:
						return inf,None
		if not self.board.possible_moves():
			return 0,None
		elif depth == 0:
			try:
				return self.eval(),None
			except:
				self.board.print()
				#self.eval(True)
				return		

		if maximizing:
			value = -inf
			moves = self.board.possible_moves()
			col = random.choice(moves)
			for move in moves:
				x,y = self.board.drop_piece(move,self.colors[True])
				og_flip = copy((self.board.until_flip))
				self.board.until_flip -= 1
				if self.board.until_flip == 0:
					self.board.flip()
					self.board.until_flip = 2
				new_val = self.minimax(depth-1,alpha,beta,False,x,y)[0]
				if og_flip == 1:
					self.board.flip()
				self.board.until_flip = og_flip
				self.board.set(x,y,0)
				if new_val > value:
					value = new_val
					col = move
				alpha = max(alpha,value)
				if alpha >= beta:
					break
			return value, col
		
		if not maximizing:
			value = inf
			moves = self.board.possible_moves()
			col = random.choice(moves)
			for move in moves:
				x,y = self.board.drop_piece(move,self.colors[False])
				og_flip = copy((self.board.until_flip))
				self.board.until_flip -= 1
				if self.board.until_flip == 0:
					self.board.flip()
					self.board.until_flip = 2
				new_val = self.minimax(depth-1,alpha,beta,True,x,y)[0]
				if og_flip == 1:
					self.board.flip()
				self.board.until_flip = og_flip
				self.board.set(x,y,0)
				if new_val < value:
					value = new_val
					col = move
				beta = min(beta,value)
				if alpha >= beta:
					break
			return value, col

					


