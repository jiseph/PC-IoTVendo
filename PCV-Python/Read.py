#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
        id, Name = reader.read()
	id, Wallet = reader.read2()
        print(id)
        print(Name)
	print(Wallet)
finally:
        GPIO.cleanup()
