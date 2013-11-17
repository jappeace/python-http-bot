#!/usr/bin/python
#this file executes the user code and calls the main functionality n times
#It also gives the name string to the functionality
from sys import argv, path
from os import getcwd
from random import choice
from bot import hyperTexter
path.append(getcwd() + '/names/')
from names import get_first_name, get_last_name

# read user input (how often to execute the code)
default = 1
if len(argv) > 1:
	loops = int(argv[1])
	loops = loops if loops > 1 else default
else:
	loops = default

# create connections
robot = hyperTexter()

looping = True
i = 0
# execute code
while looping:
	print("loop:" + str(i))
	if robot.start(get_first_name() + get_last_name()):
		i += 1
	if i >= loops:
		looping = False
