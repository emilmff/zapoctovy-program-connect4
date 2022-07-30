from ast import excepthandler
from board import Board
from math import inf
from copy import *
import random


class Minimax:

	def __init__(self, board):
		"""Creates a dictionary that knows what color we are maximizing for
		:param board: an instance of class board, that minimax is going to be working on
		:type board: Board 
		"""
		self.board = board
		self.wins = board.wins
		self.colors = {True:self.board.turn, False:-self.board.turn}
	
	def eval(self):
		"""Gives an integer score to the current state of the board, gets directions from two sides of the board, splits them into self.wins sized chunks and counts pieces in those chunks"""
		dic = {}
		for i in range(-self.wins+1,self.wins):
			dic[i] = 0
		dirs = []
		for i in range(self.board.rows):
			for j in range (-1,2):
				dirs.append(self.board.search_direction((i,0),(j,1)))
		
		for i in range(self.board.cols):
			for j in range (-1,2):				
				dirs.append(self.board.search_direction((0,i),(1,j)))
		
		for dir in dirs:
			chunks = []				
			for i in range(1,(len(dir)//self.wins)+1):
				chunks.append(dir[(i-1)*self.wins:i*self.wins])
			if len(dir)%self.wins != 0:
				chunks.append(dir[len(dir)-len(dir)%self.wins:])
			for c in chunks:
				dic[c.count(self.colors[True])] +=1
				dic[c.count(self.colors[False])]+=1

		score = 0

		for i in range(-self.wins+1,self.wins):
			if i>1:
				score += i*i*dic[i]
			elif i<-1:
				score += (-i*i -1)*dic[i]

		return score

	def minimax(self, depth, alpha, beta, maximizing,prev_row,prev_col):
		"""Minimax algorithm with alpha beta pruning, some extra handling for the flipping of the board
		:param depth: top what depth should the minimax be searching
		:type depth: int
		:param alpha: alpha for pruning
		:type alpha: int
		:param beta: beta for pruning
		:type beta: int
		:param maximizing: tells the methon whether it's currently minimizing or maximizing
		:type maximizing: Bool
		:param prev_row: row where the last piece was dropped, is necessary for the method check_for_win from Board
		:type prev_row: int
		:param prev_col: column where the last piece was dropped
		:type prev_col: int
		:rtype: (int,int)
		:return: the value of the board for the best move in the current state, the move
		"""
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
			return self.eval(),None	

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

					
