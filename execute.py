#!/usr/bin/python
import sys
import names.names

# read user input (how often to execute the code)
default = 1
if len(sys.argv) > 1:
	loops = int(sys.argv[1])
	loops = loops if loops > 1 else default
else:
	loops = default

for x in range(0, loops):
	print ('Name:' + sys.argv[0])
