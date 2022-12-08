#!/usr/bin/python3

from sys import argv
from random import randint, choice
from time import strftime, sleep
from curses import (textpad, curs_set, KEY_RIGHT, 
					KEY_LEFT, KEY_DOWN, KEY_UP, 
					wrapper, COLOR_RED)

# return the spead counter
return_the_spead_counter = True

# box_ul x, y
box_size_ul_y = 2
box_size_ul_x = 2

# box_dr x, y
box_size_dr_y = 2
box_size_dr_x = 2

# Self collision
self_collision = False

# this is time in head window
all_time = strftime('%l: %M: %S')

# this is head for snake
head_snake = ''

# this is Spead for snake
try:
	spead = int(argv[1])
except:
	spead = 25

# this is countery for spead = spead - count
snake_count = 0

# o,clock icon
o_clock_icon = ''

# food icon
food_icon = ''

# spead icon
spead_icon = ''

# snake len icon
snake_len_icon = ""

# tab betwen icon and items
tab_space = 2

# food icons
head_food = ('', '☘', '⬢', '♣', '♠')

is_live = True

def create_food(snake, box):
	"""Simple function to find coordinates of food which is inside box and not on snake body"""
	
	food = None
	while food is None:
		food = [randint(box[0][0] + 5, box[1][0] - 5),
				randint(box[0][1] + 5, box[1][1] - 5)]

		if food in snake:
			food = None

	return food

def start_new_food(stdscr, snake, box):
	food = create_food(snake, box)
	food_rend = choice(head_food)
	stdscr.addstr(food[0], food[1], f'{food_rend}') #head_food
	return food

def new_score_text(timer, score):
	return "Spead: {} {} {} Score: {} {} {} Run:{} {} {} Snake Len: {} {}".format(
			timer,
			spead_icon,
			' ' * tab_space,
			score,
			food_icon,
			' ' * tab_space,
			all_time,
			o_clock_icon,
			' ' * tab_space,
			score + 3,
			snake_len_icon)

def create_new_head(head, direction):
	if direction == KEY_RIGHT:
		new_head = [head[0], head[1] + 1]

	elif direction == KEY_LEFT:
		new_head = [head[0], head[1] - 1]

	elif direction == KEY_DOWN:
		new_head = [head[0] + 1, head[1]]

	elif direction == KEY_UP:
		new_head = [head[0] - 1, head[1]]

	return new_head


def main(stdscr):
	global is_live

	# initial settings
	curs_set(0)

	stdscr.nodelay(0)
	stdscr.timeout(100)

	# Create a game box
	sh, sw = stdscr.getmaxyx()
	box = ((box_size_ul_y, box_size_ul_x), 
		   (sh - box_size_dr_y, sw - box_size_dr_x))

	textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
	
	# create snake and set initial direction
	snake = [[sh // 2, sw // 2 + 1],
			[sh // 2, sw // 2],
			[sh // 2, sw // 2 - 1]]

	direction = KEY_RIGHT

	# this spead for snake
	timer = spead

	score = 0

	# Create startup food
	food = start_new_food(stdscr, snake, box)

	# print result of game
	stdscr.addstr(1, sw // 2 - len(new_score_text(timer, score)) // 2, new_score_text(timer, score))

	while True:
		try:
			# non-blocking input
			key = stdscr.getch()
		except KeyboardInterrupt:
			print("Good Bay!")
			exit(1)

		# find next position of snake head
		head = snake[0]

		if (is_live):
			# set direction if user pressed any arrow key
			if key in (KEY_DOWN, KEY_UP) and score > 0:
				stdscr.timeout(timer + timer)

			elif key in (KEY_RIGHT, KEY_LEFT) and score > 0:
				stdscr.timeout(timer)

			if key in (KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP):
				direction = key

			new_head = create_new_head(head, direction)

			# insert and print new head
			stdscr.addstr(new_head[0], new_head[1], head_snake)
			snake.insert(0, new_head)
			
			# if sanke head is on food
			if snake[0] == food:
				## update score
				score += 1
				if (score % 10 == 0):
					timer += 1
					stdscr.timeout(timer)

				stdscr.addstr(1, sw // 2 - len(new_score_text(timer, score)) // 2, new_score_text(timer, score))

				# create new food
				food = start_new_food(stdscr, snake, box)
			else:
				# shift snake's tail
				stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
				snake.pop()

		# conditions for game over
		if (snake[0][0] in (box[0][0], box[1][0]) or
			snake[0][1] in (box[0][1], box[1][1])):
			msg = "Game Over!\nPresse [Ctrl+C] to Quit."

			stdscr.addstr(sh // 2, sw // 2, msg)
			is_live = False

		elif self_collision and snake[0] in snake[1:]:
			msg = "Self Collision!\nPresse [Ctrl+C] to Quit."

			stdscr.addstr(sh // 2, sw // 2 // 2, msg)
			is_live = False

if __name__ == "__main__":
	# Uncomment this if you'r using Tilix Terminal with full-screen option
	#sleep(0.3)
	wrapper(main)
