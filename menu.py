from turtle import screensize
from gameloop import *

class UI:

	def __init__(self):
		"""Creates a pygame screen, creates fonts
		"""
		pygame.init()
		self.screen = pygame.display.set_mode((800,600))
		pygame.display.set_caption('CONNECT 4T')
		self.font0 = pygame.font.SysFont("arial", 30)
		self.font1 = pygame.font.SysFont("arial", 45)
		self.font2 = pygame.font.SysFont("arial", 60)
		self.font3 = pygame.font.SysFont('arial', 90)

	def draw_text(self,text, font, color, surface, x, y):
		'''Displays text on a pygame screen
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
		'''
		textobj = font.render(text, 1, color)
		text_rectangle = textobj.get_rect()
		text_rectangle.topleft = (x, y)
		surface.blit(textobj, text_rectangle)

	def size_menu(self):
		"""Creates buttons, for selecting the size of the board through the console and selecting the parameter wins for the board"""
		r= 6
		c = 7
		wins = 4
		click = False
		self.screen.fill(CYAN)
		self.draw_text('WHAT SIZE BOARD DO YOU WANT?', self.font1, BLACK, self.screen, 100, 20)
		self.draw_text('IF YOU WANT BASE SETTINGS, PRESS CONTINUE', self.font0, BLACK, self.screen, 100, 100)
		continue_button = pygame.Rect(200,200,385,100)
		pygame.draw.rect(self.screen,RED,continue_button)
		self.draw_text('CONTINUE', self.font3, BLACK, self.screen, 200, 200)
		custom_button = pygame.Rect(450,380,330,100)
		pygame.draw.rect(self.screen,RED,custom_button)
		self.draw_text('CUSTOM', self.font3, BLACK, self.screen, 460, 380)
		self.draw_text('HOW MANY WIN?', self.font1, BLACK, self.screen, 0, 450)
		connectN_button = pygame.Rect(0,500,330,100)
		pygame.draw.rect(self.screen,BLUE,connectN_button)
		self.draw_text('connectN', self.font3, RED, self.screen, 0, 500)
		while True:
			mx, my = pygame.mouse.get_pos()

			if continue_button.collidepoint((mx,my)):
				if click:
					return r,c,wins
			elif custom_button.collidepoint((mx,my)):
				if click:
					rows = int(input("enter how many rows you want: "))
					cols = int(input("enter how many columns you want: "))
					if rows>0 and cols>0:
						r= rows
						c = cols
			elif connectN_button.collidepoint((mx,my)):
				if click:
					w = int(input("how many do you want to be connecting?: "))
					if w>1:
						wins = w
			
			click = False

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True
			pygame.display.update()
			
	
	def player_menu(self):
		"""Asks whether the user wants to go first in the game"""
		click = False
		self.screen.fill(CYAN)
		self.draw_text('DO YOU WANT TO GO FIRST?', self.font2, BLACK, self.screen, 50, 20)
		yes_button = pygame.Rect(200,200,200,100)
		pygame.draw.rect(self.screen,RED,yes_button)
		self.draw_text('YES', self.font3, BLACK, self.screen, 200, 200)
		no_button = pygame.Rect(500,300,123,100)
		pygame.draw.rect(self.screen,RED,no_button)
		self.draw_text('NO', self.font3, BLACK, self.screen, 500, 300)

		while True:
			mx, my = pygame.mouse.get_pos()

			if yes_button.collidepoint((mx,my)):
				if click:
					return True
			elif no_button.collidepoint((mx,my)):
				if click:
					return False 
			
			click = False

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True
			pygame.display.update()
	
	def ai_menu(self):
		"""Gives the user the ability to choose what difficulty he wants to play"""
		click = False
		self.screen.fill(CYAN)
		draw_text('SELECT DIFFICULTY', self.font2, BLACK, self.screen, 160, 20)
		easy_button = pygame.Rect(200,150,150,70)
		pygame.draw.rect(self.screen,RED,easy_button)
		self.draw_text('EASY',self.font2,BLACK,self.screen,210,150)
		medium_button = pygame.Rect(400,237,220,70)
		pygame.draw.rect(self.screen,RED,medium_button)
		self.draw_text('MEDIUM',self.font2,BLACK,self.screen,410,237)
		hard_button = pygame.Rect(177,311,150,70)
		pygame.draw.rect(self.screen,RED,hard_button)
		self.draw_text('HARD',self.font2,BLACK,self.screen,183,311)
		custom_button = pygame.Rect(333,417,230,70)
		pygame.draw.rect(self.screen,RED,custom_button)
		self.draw_text('CUSTOM',self.font2,BLACK,self.screen,343,417)
		while True:
			mx,my = pygame.mouse.get_pos()

			if easy_button.collidepoint((mx,my)):
				if click:
					return Random_player()
			
			if medium_button.collidepoint((mx,my)):
				if click:
					return Minimax_player(3)
			
			if hard_button.collidepoint((mx,my)):
				if click:
					return Minimax_player(7)
			
			if custom_button.collidepoint((mx,my)):
				if click:
					depth = int(input("ENTER THE DEPTH OF MINIMAX YOU WANT TO PLAY AGAINST BETWEEN 1 AND 9:"))
					if 0<depth and depth<10:
						return Minimax_player(depth)
			click = False

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True
			pygame.display.update()
	
	def end_screen(self):
		"""Gives the user the ability to play again or exit once the game ends
		"""
		click = False
		self.screen.fill(CYAN)
		self.draw_text('PLAY AGAIN?', self.font2, BLACK, self.screen, 100, 20)
		yes_button = pygame.Rect(200,200,200,100)
		pygame.draw.rect(self.screen,RED,yes_button)
		self.draw_text('YES', self.font3, BLACK, self.screen, 200, 200)
		no_button = pygame.Rect(350,400,123,100)
		pygame.draw.rect(self.screen,RED,no_button)
		self.draw_text('NO', self.font3, BLACK, self.screen, 360, 400)

		while True:
			mx, my = pygame.mouse.get_pos()

			if yes_button.collidepoint((mx,my)):
				if click:
					g = UI()
					g.game_launcher()
			elif no_button.collidepoint((mx,my)):
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

	def game_launcher(self):
		"""Puts all the menu functions together and launches a game"""
		rows,cols,wins = self.size_menu()
		human_start = self.player_menu()
		opponent = self.ai_menu()
		if human_start:
			g = Game_Loop(Human_player(),opponent,1,rows,cols,wins) 
		else:
			g = Game_Loop(Human_player(),opponent,-1,rows,cols,wins)
		g.loop()
		self.end_screen()



def main():
	uu = UI()
	uu.game_launcher()
		
main()
