from random import choice
from os import system
from time import sleep
from pyfiglet import figlet_format
from termcolor import colored

#global value count to keep track of no. of moves
count = 9
x = 'x'
y = 'o'

# Draw board
def draw_bd():
	i=0
	for num in range(1,10):
		if (num % 3==0):
			print(2*(7*'_'+'|')+7*'_')
		elif num % 3 == 2:
			print(f'   {bd[i]}   |   {bd[i+1]}   |   {bd[i+2]}')
			i+=3
		else:
			print((2*(7*' '+'|')))

# Refreshing screen
def refresh():
	system("clear")
	print(colored(figlet_format('tic tae toe game'),color="red"))
	draw_bd()

# taking of User input 
def user(name,x):
	global count
	count -= 1
	p=int(input(f"{name}, enter pos for {x} in the remaining numbered positions- "))
	if p in pos:
		pos.remove(p)
		bd[p-1]=x
	else:
		print("that position is filled or out of range")
		user(name,x)
	refresh()

# returns the diagonal position
def d_pos():
	return [num for num in pos if num % 2 !=0]

# returns the non corner position
def o_pos():
	return [num for num in pos if num % 2 == 0]

# checks the equivalence of opp diagonal position
def od_pos():
	if x == bd[0] and x == bd[8]:
		return True
	elif x == bd[2] and x == bd[6]:
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
def comp(x,lv):
	global count
	op_dia = { 0 : 8, 2 : 6, 6 : 2, 8 : 0 }
	if lv == 'e':
		count -= 1
		if pos:
			p=choice(pos)
			bd[p-1]=x
			pos.remove(p)
		
	elif lv == 'm':
		count -= 1
		if check('c',x):
			refresh()
			return
		else:
			p=choice(pos)
			bd[p-1]=x
			pos.remove(p)
		
	elif lv == 'i':
		count -= 1		
		if check('c',x):
			refresh()

		elif count == 8:
			p = choice([0,2,6,8])
			bd[p] = x
			pos.remove(p+1)
			
		elif od_pos() and count == 5 and 5 not in pos:
			p=choice(o_pos())
			bd[p-1]=x
			pos.remove(p)

		elif count == 4 and 5 in pos:
			for p in d_pos():
				if p != 5:
					bd[p-1] = x
					pos.remove(p)

		elif count == 6:
			for p in [0,7]:
				if not bd[p] == y:
					break
				p = 0
			for q in [0,2,6,8]:
				if bd[q] == x:
					break
			if 5 in pos:
				if p:
					p = {0:2,2:0,6:8,8:6}[q]
				
				else:
					p = {0:6,2:8,6:2,8:2}[q]
			else:
				p = op_dia[q]
			bd[p] = x
			pos.remove(p+1)	

		elif d_pos():
			if 5 in d_pos():
				bd[4]=x
				pos.remove(5)
				refresh()
				return

			p = diamond()
			if p or p == 0:
				if p + 1 in pos:
					bd[p] = x
					pos.remove(p + 1)
					refresh()
					return
			
			p=choice(d_pos())
			bd[p-1] = x
			pos.remove(p)

		else:
			p=choice(pos)
			bd[p-1] = x
			pos.remove(p)
	refresh()
	
# verifying the equality of the slices and checking for twice occurence with status boolean that leads to winning position if any in 
# later slices
def ver(lis,st,f,x):
	if f=='w':
		if len(set(lis))==1:
			return True
		else:
			return False
	elif not st:
		if lis.count('o')==2 and 'x' not in lis:
			for n in lis:
				if n!='o':
					if x == 'o':
						st = True
						bd[n-1]=x
						pos.remove(n)
					if not st:
						pos.append(n)
					return st
		elif lis.count('x')==2 and 'o' not in lis:
			for n in lis:
				if n!='x':
					if x == 'x':
						st = True
						bd[n-1]=x
						pos.remove(n)
					if not st:
						pos.append(n)
					return st
		else:
			return None

# required slices generation
def check(f,x):
	st = False
	for num in [0,3,6]:
		if ver(bd[num:num+3],st,f,x):
			return x
	for num in range(3):
		if ver(bd[num::3],st,f,x):
				return x
	if ver(bd[0: :4],st,f,x):
		return x
	elif ver(bd[2:7:2],st,f,x):
		return x
	if (len(pos) > count+1) and f != 'w': 
#			print(f'{pos}')
			n = pos.pop() 
			bd[n-1] = x
			pos.remove(n)
			return x
	return None	

# deciding the winner
def winner(x,name):
	if x:
		if x=="x":
			#refresh()
			print(f'{name} with {x} has won')
			print(f'{pos}')
			return True
		elif x=="o":
			#refresh()
			print(f'{name} with {x} has won')
			print(f'{pos}')
			return True
	if not pos:
		refresh()
		print('match drawn')
		return True
	else:
		return False

# menu and level displaying the options
def level():
	refresh()
	ch = int(input('1->Easy\n2->Medium\n3->Impossible\nenter your level of play - '))
	if ch in range(1,4):	
		if ch == 1:
			lv = 'e'
		elif ch == 2:
			lv = 'm'
		else:
			lv = 'i'
		return lv
	else:
		print('wrong choice!!!!enter again')
		sleep(2)
		level()
	
def menu(lv):
	refresh()
	print('1) 2 players\n2) 1 player with x\n3) 1 player with o\n4) system against itself')
	n=int(input('enter your choice- '))
	if n in range(1,5):
		game(n)
	else:
		print("wrong choice!!..enter again")
		sleep(2)
		menu(lv)

# working on the chosen option
def game(ch):
	global x,y	
	while pos:
		refresh()
		
		if ch==1:
			user('player',x)
			if winner(check('w',x),'player'):
				break
			user('player',y)
			if winner(check('w',y),'player'):
				break
		elif ch==2:
			user('player',x)
			if winner(check('w',x),'player'):
				break
			sleep(2)
			comp(y,lv)
			if winner(check('w',y),'computer'):
				break
		elif ch==3:
			sleep(2)
			comp(x,lv)
			if winner(check('w',x),'computer'):
				break
			user('player',y)
			if winner(check('w',y),'player'):
				break
		else:
			sleep(2)
			comp(x,lv)
			if winner(check('w',x),'computer'):
				break
			sleep(2)
			comp(y,lv)
			if winner(check('w',y),'computer'):
				break

# initialisation and starting point	
while True:
	bd = list(range(1,10))
	pos = list(range(1,10))
	count = 9
	lv = level()
	menu(lv)
	op=input(('do you want to play again...n for no- '))
	if op=='n':
		break





