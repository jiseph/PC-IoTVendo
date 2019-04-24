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

port = "/dev/ttyUSB0" #Set the port of the RPI to read the Arduino Nano

buzzer=18 #Set the Buzzer to GPIO 18

GPIO.setwarnings(False) #Remove the warnings of the RPI
GPIO.setmode(GPIO.BCM) #Set the GPIO pins to the number given in the code
GPIO.setup(buzzer,GPIO.OUT) #Set the Buzzer to an output


serialData = serial.Serial(port, 9600) #Set the baude rate for the Rpi to read the serial of the Arduino Nano

display = I2C_LCD_driver.lcd() #Set the function of the LCD to 'display'
camera = PiCamera() #Set the function of the RPI to 'camera'
camera.resolution = (1024, 768) #Set the Camera resolution

MIFAREReader = MFRC522.MFRC522() 
reader = SimpleMFRC522.SimpleMFRC522()

str_pad = " " * 16 #Set the amount of empty blocks of the LCD
print("Program start in 3")
serialData.setDTR(True) #Start accepting serial signals
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
        seriali = serialData.readline().decode('utf-8') #Reading the Serial of the Arduino Nano
        print(seriali)
        
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL) #Confirmation checking of the read RFID
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK: #If the confirmation of the RFID passed, it will go here
            GPIO.output(buzzer,GPIO.LOW)
            print("Alarm is off")
            camera.start_preview()
            camera.capture("Client "+ str(take) + ".jpg") #RpiCamera will make a file for each taken image
            take = take+1
            camera.stop_preview() #To Remove the RPI Camera display on screen
            display.lcd_clear()
            print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])) #Print the UID on the Shell/Cmd 
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
            
            if (int(seriali)-5) > 50: #Check if the analog read from the arduino serial would correspond to the door being open or closed
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
