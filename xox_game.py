from random import choice
from os import system
from time import sleep
from pyfiglet import figlet_format
from termcolor import colored

#global value count to keep track of no. of moves
count = 9

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

def d_pos():
	return [num for num in pos if num % 2 !=0]

# computer chosen postion using random list generation-easy level play, twice occurence position for medium, twice occurence and 
# double attack positions for impossible. 
def comp(x,lv):
	global count
	count -= 1
	if lv == 'e':
		if pos:
			p=choice(pos)
			bd[p-1]=x
			pos.remove(p)
		
	elif lv == 'm':
		if check('c',x):
			refresh()
			return
		else:
			p=choice(pos)
			bd[p-1]=x
			pos.remove(p)
		
	elif lv == 'i':
		if check('c',x):
			refresh()
			return
		else:
			if 5 in d_pos():
				bd[4]=x
				pos.remove(5)
			elif d_pos():
				if bd[1] == bd[3]:
					if 0 in pos:
						bd [0] = x
						pos.remove(1)
				elif bd[1] == bd[5]:
					if 2 in pos:
						bd [2] = x
						pos.remove(3)
				elif bd[7] == bd[5]:
					if 8 in pos:
						bd [8] = x
						pos.remove(9)
				elif bd[7] == bd[3]:
					if 6 in pos:
						bd [6] = x
						pos.remove(7)
				else:
					p=choice(d_pos())
					bd[p-1]=x
					pos.remove(p)
			else:
				p=choice(pos)
				bd[p-1]=x
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
	if (len(pos)>count + 1) and f != 'w': 
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
			
			return True
		elif x=="o":
			#refresh()
			print(f'{name} with {x} has won')
		
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
	while pos:
		refresh()
		x , y = 'x' , 'o'
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
			x , y = 'o' , 'x'
			sleep(2)
			comp(y,lv)
			if winner(check('w',y),'computer'):
				break
			user('player',x)
			if winner(check('w',x),'player'):
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





