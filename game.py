import random, pygame, sys
from pygame.locals import *
from random import choice

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BW = 3 # number of columns of icons
BH = 3 # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BW * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BH * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
NAVYBLUE = ( 60,  60, 100)
D_WHITE  = (220, 220, 220)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
BLUE     = (  0,   0, 255)
GRAY     = (100, 100, 100)
BLACK    = (  0,   0,   0)

BGCOLOR = NAVYBLUE
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
XOCOLOR = RED
LIGHTBGCOLOR = GRAY

# global values used 
bd = 9 * [' ']
pos = list(range(1,10))
count = 9
x = 'x'
y = 'o'

# initialise pygaem and set caption
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Tic Toc Tae Game')

# initialise font
pygame.font.init()
myf=pygame.font.Font("freesansbold.ttf",20)

# change symbol for play when x button is clicked
def X(l):
	if 'p' in l:
		global x,y
		x = 'x'
		y = 'o'
		if count != 9:
			new_game()

# change symbol for play when o button is clicked
def Y(l):
	if 'p' in l:
		global x,y
		x = 'o'
		y = 'x'
		if count != 9:
			new_game()

# exit function when quit is clicked
def exit():
	pygame.quit()
	quit()

# text object creation
def text_objects(text,	font,color):
	t_surf	=	font.render(text,	True,	color)
	return	t_surf,	t_surf.get_rect()

# display of text function
def message_display(text,x =320,y =	330,size=20,color = BLACK):
	myf=pygame.font.Font("freesansbold.ttf",size)
	t_surf,	t_rect	=	text_objects(text,	myf,color)
	t_rect.center	=	(x,	y)
	DISPLAYSURF.blit(t_surf,	t_rect)

# button function for the game
def button(msg,x,y,w,h,ic,ac,action = None, lv = None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(DISPLAYSURF, ac,(x,y,w,h))
		if click[0] == 1 and action != None:
			if lv != None:
				action(lv)
			else:
				action()
	else:
		pygame.draw.rect(DISPLAYSURF, ic,(x,y,w,h))

	message_display(msg,x + w/2,y + h/2, 15)

# menu display function
def display_menu():
	new_game()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		DISPLAYSURF.fill(BGCOLOR)
		message_display('Tic Tac Toe',WINDOWWIDTH/2,YMARGIN/2,25,WHITE)

		button("2 Players",50,YMARGIN,150,50,D_WHITE,WHITE,main,'nc')		
		button("1 Player",(WINDOWWIDTH - 200),YMARGIN,150,50,D_WHITE,WHITE,level,'p')
		button("System vs itself",50,YMARGIN*2,150,50,D_WHITE,WHITE,level,'s')	
		button("Quit",(WINDOWWIDTH - 200),YMARGIN*2,150,50,D_WHITE,WHITE,exit)		
		pygame.display.update()
		FPSCLOCK.tick(FPS)

# level display function
def level(lv):
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		DISPLAYSURF.fill(BGCOLOR)
		message_display('Tic Tac Toe',WINDOWWIDTH/2,YMARGIN/2,25,WHITE)
		button("Easy",50,YMARGIN*.7,150,50,D_WHITE,WHITE,main,lv+'e')
		button("Medium",(WINDOWWIDTH - 200),YMARGIN*.7,150,50,D_WHITE,WHITE,main,lv+'m')
		button("Impossible",50,YMARGIN*1.6,150,50,D_WHITE,WHITE,main,lv+'i')
		button("Back",(WINDOWWIDTH - 200),YMARGIN*1.6,150,50,D_WHITE,WHITE,display_menu)
		pygame.display.update()

# new game function that resets everything
def new_game():
	global bd,pos,count,x,y
	bd = 9 * [' ']
	pos = list(range(1,10))
	count = 9
	x = 'x'
	y = 'o'

# player loop
def player(mx,my,s,l):
	while not user(mx,my,s):
		main(l)
	w = winner(check('w',s),'player')
	if (w):
		end_game(s,'player')
	elif not pos and not w:
		end_game(w,'player')
	return

# computer loop
def computer(s,l):
	comp(s,l)
	w = winner(check('w',s),'computer')
	if (w):
		end_game(s,'computer')
	elif not pos and not w:
		end_game(w,'player')				

# main game loop
def main(lv):
	global FPSCLOCK, DISPLAYSURF,x,y
		
	DISPLAYSURF.fill(BGCOLOR)
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		draw_bd(lv)
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if click [0] == 1:
			if lv == 'nc':							# 2 players game loop
				player(mouse[0],mouse[1],x,lv)
				x, y = y ,x
			if 'p' in lv:							# player vs system game loop
				if x == 'x':
					player(mouse[0],mouse[1],x,lv)
					computer(y,lv)
				else:
					if count % 2 == 0:
						player(mouse[0],mouse[1],x,lv)
		if count % 2 != 0 and 'p' in lv and x == 'o':
			computer(y,lv)
		if 's' in lv:							# system vs system game loop
			computer(x,lv)
			x, y = y ,x

		pygame.display.update()
	
# verifying the equality of the slices and checking for twice occurence with status boolean that leads to winning position if any in 
# later slices
def ver(lis,st,s,inf,f,x):
	if f=='w':
		if len(set(lis))==1 and x in lis:
			return True
		else:
			return False
	elif not st:
		if lis.count('x')==2 and 'o' not in lis:
			for n in lis:
				if n!='x':
					if x == 'x':
						st = True
						bd[(inf*lis.index(n))+s]=x
						
						pos.remove((inf*lis.index(n))+s+1)
					if not st:
						pos.append((inf*lis.index(n))+s)
					return st
		elif lis.count('o')==2 and 'x' not in lis:
			for n in lis:
				if n!='o':
					if x == 'o':
						st = True
						bd[(inf*lis.index(n))+s]=x
						
						pos.remove((inf*lis.index(n))+s+1)
					if not st:
						pos.append((inf*lis.index(n))+s)
					return st
	return False

# required slices generation
def check(f,x):
	st = False
	for num in [0,3,6]:
		if ver(bd[num:num+3],st,num,1,f,x):
			return x
	for num in range(3):
		if ver(bd[num::3],st,num,3,f,x):
			return x
	if ver(bd[0: :4],st,0,4,f,x):
		return x
	elif ver(bd[2:7:2],st,2,2,f,x):
		return x
	
	if (len(pos) > count+1) and f != 'w': 
		n = pos.pop() 
		bd[n] = x
		pos.remove(n+1)
		return x
	return None

# returns the diagonal position
def d_pos():
	return [num for num in pos if num % 2 !=0]

# returns the non corner position
def o_pos():
	return [num for num in pos if num % 2 == 0]

# checks the equivalence of opp diagonal position
def od_pos():
	if 'x' == bd[0] and 'x' == bd[8]:
		return True
	elif 'x' == bd[2] and 'x' == bd[6]:
		return True
	else:
		return False

# checks the equivalence of non corner positions
def diamond():
	for n in [3,5]:
		if bd[1] == bd[n]:
			return n - 3
		if bd[7] == bd[n]:
			return n + 3
	return None

# computer chosen postion using random list generation-easy level play, twice occurence position for medium, twice occurence and 
# double attack positions for impossible. 
def comp(x,l):
	global count
	if 'e' in l:
		count -= 1
		if pos:
			p=choice(pos)
			bd[p-1]=x
			pos.remove(p)
	elif 'm' in l:
		count -= 1
		if check('c',x):
			
			return
		else:
			p=choice(pos)
			bd[p-1]=x
			pos.remove(p)
	elif 'i' in l:
		op_dia = { 0 : 8, 2 : 6, 6 : 2, 8 : 0 }
		count -= 1		
		if check('c',x):
			return
		
		elif count == 8:
			p = choice([0,2,6,8])
			bd[p] = x
			pos.remove(p+1)
			
		elif od_pos() and count == 5 and 5 not in pos:
			p=choice(o_pos())
			bd[p-1]=x
			pos.remove(p)

		elif count == 4 and 5 in pos:
				if len(d_pos()) == 2:
					for p in d_pos():
						if p != 5:
							bd[p-1] = x
							pos.remove(p)
				else:
					p = diamond()
					p = op_dia[p]
					bd[p] = x
					pos.remove(p+1)

		elif count == 6:
			for q in [0,2,6,8]:
				if bd[q] == x:
					break
			if 5 in pos:
				for p in range(9):
					if  bd[p] == y:
						if p in [1,7]:
							p = {0:6,2:8,6:2,8:2}[q]
						elif p in [3,5]:
							p = {0:2,2:0,6:8,8:6}[q]
						elif op_dia[q] == p:
							p = {0:2,2:0,6:8,8:6}[q]
						else:
							p = op_dia[p]
						break
			else:
				p = op_dia[q]
			bd[p] = x
			pos.remove(p+1)	

		elif d_pos():
			if 5 in d_pos():
				bd[4]=x
				pos.remove(5)
				return

			p = diamond()
			if p or p == 0:
				if p + 1 in pos:
					bd[p] = x
					pos.remove(p + 1)
					return
			
			p=choice(d_pos())
			bd[p-1] = x
			pos.remove(p)

		else:
			p=choice(pos)
			bd[p-1] = x
			pos.remove(p)

# taking user input
def user(mousex,mousey,x):
	global count
	bx,by = get_pos(mousex,mousey)
	if bx != None and by != None:
		p = (3 * by) + (bx + 1)
		if p in pos:
				bd[p-1] = x
				pos.remove(p)
				DISPLAYSURF.fill(BGCOLOR)
				draw_bd()
				count -= 1
				return True
	return False

# Convert board coordinates to pixel coordinates
def lt_coord(bx,by):
	left = bx * (BOXSIZE + GAPSIZE) + XMARGIN
	top = by * (BOXSIZE + GAPSIZE) + YMARGIN
	return (left, top)

# return position if it collides with the board position
def get_pos(x,y):
	for by in range (BH):
		for bx in range (BW):
			left, top = lt_coord(bx, by)
			boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
			if boxRect.collidepoint(x, y):
				return (bx, by)
	return (None, None)

# draw symbol x and o
def draw_ox(p,lt,tp,bd):
	hs = 0.5*BOXSIZE
	message_display(bd[p],lt+hs,tp+hs)

# draw 3x3 board 			
def draw_bd(lv = None):
	for by in range(BW):
		for bx in range(BH):
			left,top = lt_coord(bx,by)
			p = by * 3 + bx
			pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
			draw_ox(p,left,top,bd)
			message_display('Tic Tac Toe',WINDOWWIDTH/2,YMARGIN/2,25,WHITE)
			button("new game",(WINDOWWIDTH*.2)-50,WINDOWHEIGHT/6,100,40,D_WHITE,WHITE,new_game)
			button("quit",(WINDOWWIDTH*.8)-50,WINDOWHEIGHT/6,100,40,D_WHITE,WHITE,exit)
			button("X",(WINDOWWIDTH*.2)-50,4*WINDOWHEIGHT/6,100,40,D_WHITE,WHITE,X,lv)
			button("O",(WINDOWWIDTH*.8)-50,4*WINDOWHEIGHT/6,100,40,D_WHITE,WHITE,Y,lv)
			button("Main menu",(WINDOWWIDTH*.5)-50,5*WINDOWHEIGHT/6,100,40,D_WHITE,WHITE,display_menu)

	pygame.time.wait(100)

# deciding the winner
def winner(x,name):
	if x:
		if x=="x":
			message_display(f'{name} with {x} has won',320,330,20,XOCOLOR)
			return x
		elif x=="o":
			message_display(f'{name} with {x} has won',320,330,20,XOCOLOR	)
			return x
	elif not pos:
		message_display('match drawn',320,330,20,XOCOLOR)
		return None
	else:
		return False

# shows game result repeatedly for some time until the menu shows up again
def end_game(x,win):
	global bd,pos,count
	color1 = LIGHTBGCOLOR
	color2 = BGCOLOR

	for i in range(13):
		color1, color2 = color2, color1 # swap colors
		DISPLAYSURF.fill(color1)
		draw_bd()
		winner(x,win)
		pygame.display.update()
		pygame.time.wait(300)
	new_game()
	display_menu()

# starting point of the program 
if __name__ == '__main__':
	display_menu()
	
