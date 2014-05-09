#!/usr/bin/env python
"""
LCD-like clock with 24h/12h switch.

"""
import os
import argparse

from datetime import datetime, timedelta
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


def draw(midday=False):
	time = get_time()

	if midday:
		text = "am"
		hour = int(time[:2])
		if hour > 12:
			text = "pm"
			time = "{0:02d}{1}".format(hour-12, time[2:])

	for row in range(1,4):
		line = [show(digit,row) for digit in time]
		if midday and row == 2:
			print "".join(line) + " " + text
		else:
			print "".join(line)


while True:
	parser = argparse.ArgumentParser()
	parser.add_argument("-m", "--midday", action="store_true", help="enable 12h clock")
	args = parser.parse_args()

	draw(args.midday)
	sleep(0.5)
	os.system("clear")
