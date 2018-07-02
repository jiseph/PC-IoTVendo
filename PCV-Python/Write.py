#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
reader = SimpleMFRC522.SimpleMFRC522()
def goto(linenum):
	global line
	line = linenum

try:
	line = 1
	while True:
		if line == 1:
			Wallet = raw_input('Enter Wallet:')
			print("You have entered:")
			print(Wallet + "\n\n")
			print("Is this information correct?")
			Answer = raw_input('Y/N:')
			if (Answer == "Y") or (Answer == "y"):
                                print("Now place your tag to write")
				reader.write(Wallet)
                                print("Written")
				id, Wallet = reader.read()
				break
			elif (Answer == 'N') or (Answer == 'n'):
				goto(1)
finally:
        GPIO.cleanup()
