from threading import Thread
import RPi.GPIO as GPIO
import requests

DOOR_SWITCH = 23

GPIO.setmode(GPIO.BOARD)
GPIO.setup(DOOR_SWITCH, GPIO.IN)

# Global States

global cycle
cycle = 0.0
# Door Switch
global isDoorClosed
isDoorClosed = True

# User Scanning State
global isScanning
isScanning = False

# LCD States
global isDefault
isDefault = True

# Time to Open Door
global isTimeToOpenDoor
isTimeToOpenDoor = False

# Door Opened
global isDoorOpened
isDoorOpened = False

global GroceryCart

global isTimeToScan
isTimeToScan = False

global isInvalidUUID
isInvalidUUID = False


class GroceryCart:
    self.currentUUID = None
    self.groceryItems = []

    def addItem(item):
        
        self.groceryItems.add(item)

    def reset():
        self.currentUUID = None
        self.groceryItems = []

    def __str__(self):
        return "UUID {} : Grocery Items: {}".format(self.currentUUID, str([for groceryItem in groceryItems]))

# LCD init
def lcd_init():
    # TODO: LCD variables here
    pass

# TODO: more lcd function

def lcd_string(message, line):
    pass

def checkIfUUIDexists(uuid=None):
    # if uuid:
    #     requests.get(
    #         'https://vendo.gameworks.io/check/{}'.format(uuid)
    #     )
    return True

def sound_alarm():
    pass

def trigger_door_opened_callback(channel):
    if GroceryCart.currentUUID:
        isTimeToScan = True
    else:
        sound_alarm()


class BaseThread(Thread):

    self._running = False

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        pass
    

class LCDThread(BaseThread):
    """ Thread for LCD displays """
    
    def __init__(self):
        self._running = True
        lcd_init()

    def run(self):
        global cycle
        global isInvalidUUID
        global isTimeToOpenDoor
        global isTimeToScan
        
        isDefaultWelcome = True

        while self._running:

            # Is Default State
            if isDefault:
                time.sleep(3)
                # LCD Display on Default
                if isDefaultWelcome:
                    lcd_string("Welcome", 1)
                    isDefaultWelcome = False
                else:
                    lcd_string("Scan", 1)
                    isDefaultWelcome = True
            elif isInvalidUUID:
                # Is Door Opened
                lcd_string("Invalid UUID. Please try again!", 1)
            elif isTimeToOpenDoor:
                # Scanned UUID but hasn't opened the door
                lcd_string("Open Door", 1)
            elif isTimeToScan:
                # Scan Item
                lcd_string("Scan Item")


                      
                

class RFIDThread(BaseThread):
    """ Thread for RFID Scans """

    def __init__(self):
        self._running = True

    def run(self):
        # threading cycle
        global cycle
        global isTimeToOpenDoor
        global isDefault
        global isInvalidUUID

        start = None

        while self._running:
            

            # Constantly read for uuid
            uuid = reader.read()

            # If a uuid is read
            if uuid:
                if checkIfUUIDexists(uuid):

                    # Time to open the door :)
                    isTimeToOpenDoor = True
                    # Assign read uuid to currentUUID (stored globally)
                    GroceryCart.currentUUID = uuid
                else:
                    # Change Screen (disable default messages)
                    isDefault = False
                    # Invalid UUID
                    isInvalidUUID = True
            elif isTimeToScan:
                # Barcode Scanner Input Stream Reader / Callback function
                if GroceryCart.groceryItems and not start:
                    start = time.time()
                elif (time.time() - start >= 10):
                    isTimeToScan = False
                    isEndTransaction = True
                    # Its either we tapout (and give 1 minute grace period
                    # before forced logout) or timeout within 45 seconds without need to tapout


                    


                


                

                


            



