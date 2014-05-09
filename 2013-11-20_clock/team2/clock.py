#!/usr/bin/env python
"""
LCD-like clock. Basic version.

"""
import os

from datetime import datetime
from time import sleep

digits = {
	"9": "010111011",
	"8": "010111111",
	"7": "010001001",
	"6": "010110111",
	"5": "010110011",
	"4": "000111001",
	"3": "010011011",
	"2": "010011110",
	"1": "000001001",
	"0": "010101111",
}

def show(digit, row):
	if digit == " ":
		return "  "

	code = digits[digit][(row-1)*3:row*3]
	edge = lambda x: " " if x == "0" else "|"
	middle = lambda x: " " if x == "0" else "_"
	return edge(code[0]) + middle(code[1]) + edge(code[2])

def get_time():
	now = datetime.now()
	return "{0:02d} {1:02d} {2:02d}".format(now.hour, now.minute, now.second)

def draw():
	time = get_time()
	for row in range(1,4):
		line = [show(digit,row) for digit in time]
		print "".join(line)

while True:
	draw()
	sleep(0.5)
	os.system("clear")
