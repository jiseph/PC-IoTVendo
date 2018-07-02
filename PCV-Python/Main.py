import time
import RPi.GPIO as GPIO
import MFRC522
import SimpleMFRC522
import smbus
import I2C_LCD_driver
import time
import serial
from picamera import PiCamera
from time import sleep

port = "/dev/ttyUSB0"

buzzer=18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)


serialData = serial.Serial(port, 9600)

display = I2C_LCD_driver.lcd()
camera = PiCamera()
camera.resolution = (1024, 768)

MIFAREReader = MFRC522.MFRC522()
reader = SimpleMFRC522.SimpleMFRC522()

str_pad = " " * 16
print("Program start in 3")
serialData.setDTR(True)
sleep(1)
print("2")
sleep(1)
print("1")
sleep(1)

choice = 1
take = 1

try:
  while True:

    if (serialData.inWaiting()>0):
        seriali = serialData.readline().decode('utf-8')
        print(seriali)
        
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            GPIO.output(buzzer,GPIO.LOW)
            print("Alarm is off")
            camera.start_preview()
            camera.capture("Client "+ str(take) + ".jpg")
            take = take+1
            camera.stop_preview()
            display.lcd_clear()
            print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
            display.lcd_display_string("RFID Read!",1)
            sleep(2)
            display.lcd_clear()
            display.lcd_display_string("Proceed with",1)
            display.lcd_display_string("transaction",2)
            sleep(3)
            display.lcd_clear()
            serialData.setDTR(True)
            choice = 1
            
        else:
            display.lcd_display_string("Place RFID on",1)
            display.lcd_display_string("the scanner",2)
            
            if (int(seriali)-5) > 50:
                print ("Door is closed without scanning")
                GPIO.output(buzzer,GPIO.LOW)
                print("Alarm is off")
            else:
                print("Door Opened without scanning")
                GPIO.output(buzzer,GPIO.HIGH)
                print("Alarm is on")

 
except KeyboardInterrupt:
    GPIO.cleanup()
    display.lcd_clear()