from asyncore import close_all
from operator import ilshift, truediv


class Board:

    def __init__(self, m = 6, n = 7, start = 1, wins = 4,until_flip = 2):
        self.rows = m
        self.cols = n
        self.initialize_board()
        self.orientation = True
        self.wins = wins
        self.turn = start
        self.until_flip = until_flip

    def change_turn(self):
        self.turn = -self.turn

    def flip(self):
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
        self.board = []
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[i].append(0)
        return self

    def print(self):
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
        return self.board[row][col]
    
    def set(self,row,col,val):
        self.board[row][col] = val
        return self

    def in_range(self,row = None,col = None):
        if row is not None and col is not None:
            return 0<=row<self.rows and 0<=col<self.cols
        if row is not None:
            return 0<=row<self.rows
        if col is not None:
            return 0<=col<self.cols

    def search_direction(self, start, dir):
        x,y = start
        dir_x,dir_y = dir 
        out = []
        while self.in_range(x,y):
            out.append(self.get(x,y))
            x += dir_x
            y += dir_y
        return out
      
    def is_dropable(self,col):
        return self.search_direction((0,col),(1,0))[0] == 0

    def check_for_win(self,row,col,color,debug=False):
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
        if debug:
            print(dirs)
        for dir in dirs:
            count = 0
            for num in dir:
                if num == color:
                    count+=1              
                if count >=4:   
                    return True
                if num != color:
                    count = 0
        return False

    def possible_moves(self):
        out = []
        for i in range(self.cols):
            if self.is_dropable(i):
                out.append(i)
        return out

    def drop_piece(self,col,color):
        if self.in_range(None,col):
            cesta = self.search_direction((0,col),(1,0))
            i= 0
            while i < self.rows and cesta[i] == 0:
                i+=1
            self.set(i-1,col,color)
            return i-1,col

        