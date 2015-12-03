#!/usr/bin/python
from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime
from time import sleep, strftime
from subprocess import *
import os, twitter

# This is different depending on your wiring
LCD_PINS = [23, 17, 18, 22]

LCD_CHAR_WIDTH = 16
LCD_CHAR_MAX_LEN = 40

# Twitter key stuff, set as environment variables
# in the supervisor config file
CON_KEY = os.environ.get("CONSUMER_KEY")
CON_SEC = os.environ.get("CONSUMER_SECRET")
ACC_KEY = os.environ.get("ACCESS_TOKEN_KEY")
ACC_SEC = os.environ.get("ACCESS_TOKEN_SECRET")

TWITTER_ACC_NAME = "BoredElonMusk"
COUNT = 1 # Number of tweets to fetch
WAIT_TIME = 60 * 5 # sec, time between refresh
SCROLL_DELAY = 0.25 # sec 

api = twitter.Api(consumer_key=CON_KEY,
	consumer_secret=CON_SEC,
	access_token_key=ACC_KEY,
	access_token_secret=ACC_SEC)

lcd = Adafruit_CharLCD(pins_db=LCD_PINS)

def get_posts():
	return api.GetUserTimeline(screen_name=TWITTER_ACC_NAME, count=COUNT)

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def get_date():
	return datetime.now().strftime("%b %d %H:%M:%S")

def split_string_median(text):
	index = 0
	words = text.split(" ")
	for i in range(1, len(words)):
		s = " ".join(words[0:i])
		if len(s) > len(text) / 2:
			index = i - 1
			break
	t1 = " ".join(words[0:index])
	t2 = " ".join(words[index:len(words)])
	return [t1, t2]

def split_s_by_length(text, split_width):
	words = text.split(" ")
	lines = []
	idx = 0
	if len(words) == 0: return None
	if len(words) == 1: return words[0]
	for i in range(1, len(words)):
		s = " ".join(words[idx:i])
		if len(s) > split_width:
			line = " ".join(words[idx:i - 1])
			idx = i - 1
			lines.append(line)
	s = " ".join(words[idx:])
	lines.append(s)
	return lines

def scroll_v(text, split_width, index, rows):
	lines = split_s_by_length(text, split_width)
	return "\n".join(lines[index:index + rows])

def scroll_h(text, width, index, check_bounds=True):
	if index < 0:
		return text[0:width]
	delta = len(text) - width
	if index > delta and check_bounds:
		return text[delta:delta + width]
	return text[index:index + width]

def main():
	lcd.begin(16,1)
	text = get_posts()[0].text
	width = 16
	lines = split_s_by_length(text, width)
	rows = 2
	index = 0
	max_index = len(text)
	while True:
		lcd.clear()
		lcd.message(TWITTER_ACC_NAME + ":\n")
		# Horizontal scroll
		lcd.message(scroll_h(text, width, index))
		# Vertical scroll
		#lcd.message(scroll_v(text, width, index, rows))
		if index == 0:
			sleep(3)

		if index < max_index:
			index += 1
		else:
			index = 0
		sleep(SCROLL_DELAY)

if __name__ == "__main__":
	main()
