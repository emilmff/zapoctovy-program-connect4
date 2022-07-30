from asyncore import close_all
from operator import ilshift, truediv


class Board:

	def __init__(self, m = 6, n = 7, start = 1, wins = 4,until_flip = 2):
		"""Just sets key variables for the Board class, and calls self.initialize_board()
		:param m: the number of rows the board will have
		:type m: int
		:param n : the number of columns the board will have
		:type n: int
		:param start: specifies the color of that player that plays first - is either 1 or -1
		:type start: int
		:param wins: how many in a row you need to win
		:type wins: int
		:param until_flip: tells the board how often it should flip
		:type until_flip: int
		"""
		self.rows = m
		self.cols = n
		self.initialize_board()
		self.orientation = True
		self.wins = wins
		self.turn = start
		self.until_flip = until_flip

	def change_turn(self):
		"""Changes the boards turn"""
		self.turn = -self.turn

	def flip(self):
		"""Transposes the matrix that represents the board
		:rtype: Board
		:return: this instance of class Board
		"""
		self.orientation = not self.orientation
		self.rows,self.cols = self.cols,self.rows
		new_board = []
		for i in range(self.rows):
			new_board.append([])
			for j in range(self.cols):
				new_board[i].append(self.board[j][i])
		self.board = new_board
		return self

	def initialize_board(self):
		"""Transposes the matrix that represents the board
		:rtype: Board
		:return: this instance of class Board
		"""
		self.board = []
		for i in range(self.rows):
			self.board.append([])
			for j in range(self.cols):
				self.board[i].append(0)
		return self

	def print(self):
		"""Prints out the board without brackets and replaces the color -1 with 2, for alignment
		:rtype: Board
		:return: this instance of class Board
		"""
		for i in self.board:
			for j in i:
				if j == -1:
					print(2,end= ' ')
				else: 
					print(j,end = ' ')
			print()
		print()
		return self
	
	def get(self,row,col):
		"""Returns the value on the board at the position row,col
		:param row: which row is the value in
		:type row: int
		:param col: which col is the value in
		:type col: int
		:rtype: int
		:return: value in board at row,col
		"""
		return self.board[row][col]
	
	def set(self,row,col,val):
		"""Sets value at row, col in board to val
		:param row: which row we want val in
		:type row: int
		:param col: which col we want val in
		:type col: int
		:param val: what are we setting board[row][col] to
		:type val: int
		:rtype: Board
		:return: this instance of class Board
		"""
		self.board[row][col] = val
		return self

	def in_range(self,row = None,col = None):
		"""Checks if coordinates are on the board
		:param row: a number
		:type row: int
		:param col: a number
		:type col: int
		:rtype: bool
		:return: returns True if the parameters are in range
		"""
		if row is not None and col is not None:
			return 0<=row<self.rows and 0<=col<self.cols
		if row is not None:
			return 0<=row<self.rows
		if col is not None:
			return 0<=col<self.cols

	def search_direction(self, start, dir):
		"""Fills a list with the numbers from a starting location in a direction
		:param start: the row and column the search starts from
		:type start: (int,int)
		:param dir: the direction which we are searching: "a vector"
		:type dir: (int,int)
		:rtype: list
		:return: list of all values on the board in the given direction, includes the value of the starting point
		"""
		x,y = start
		dir_x,dir_y = dir 
		out = []
		while self.in_range(x,y):
			out.append(self.get(x,y))
			x += dir_x
			y += dir_y
		return out
	  
	def is_dropable(self,col):
		"""Checks is there is a vacant spot on the top of a column
		:param col: the column we want to check
		:type col: int
		:rtype: bool
		:return: True if is vacant, else False
		"""
		return self.search_direction((0,col),(1,0))[0] == 0

	def check_for_win(self,row,col,color):
		"""This function uses the search_direction method to check all 8 directions around the spot we want to be checking the win from, then it merges them into 4 lists and proceeds to try to find self.wins in a row in them
		:param row: the row we search from
		:type row: int
		:param col: the column we search from
		:type col: int
		:param color: the color we are checking for win for
		:type color: int
		:rtype: Bool
		:return: True if there are self.wins in a row, else False
		"""
		dirs = []
		for i in range(-1,1):
			for j in range(-1,1):
				if i!=0 or j != 0:
					first_part =self.search_direction((row,col),(i,j))
					first_part.reverse()
					dirs.append(first_part+self.search_direction((row,col),(-i,-j))[1:])
		first_part = self.search_direction((row,col),(1,-1))
		first_part.reverse()
		dirs.append(first_part+self.search_direction((row,col),(-1,1))[1:])
		for dir in dirs:
			count = 0
			for num in dir:
				if num == color:
					count+=1              
				if count >=self.wins:   
					return True
				if num != color:
					count = 0
		return False

	def possible_moves(self):
		"""This function is specifically for minimax, so that you can easily acces all possible moves
		:rtype: list
		:return: all the columns where you can drop a piece
		"""
		out = []
		for i in range(self.cols):
			if self.is_dropable(i):
				out.append(i)
		return out

	def drop_piece(self,col,color):
		"""Drops a piece onto the board and returns the location where it fell
		:param col: the column we drop in 
		:type col: int
		:param color: the color to be dropped
		:type color: int
		:rtype: (int,int)
		:return: the row and column where the piece dropped
		"""
		if self.in_range(None,col):
			cesta = self.search_direction((0,col),(1,0))
			i= 0
			while i < self.rows and cesta[i] == 0:
				i+=1
			self.set(i-1,col,color)
			return i-1,col

		