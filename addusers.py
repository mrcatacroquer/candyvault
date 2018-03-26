import sys
import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep
from mysqlhelper import MYSQLHelper

DB = MYSQLHelper()

continue_reading = True


MIFAREReader = MFRC522.MFRC522()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
pwm=GPIO.PWM(32, 50)
pwm.start(0)

print "Starting read..."
print "Press Ctrl-C to stop."

while continue_reading:
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if not status == MIFAREReader.MI_OK:
        continue

    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status is not MIFAREReader.MI_OK or len(uid) < 4:
        continue

    carduid = str(uid[0]) +","+ str(uid[1]) +","+ str(uid[2]) +","+ str(uid[3]) +","+ str(uid[4])

    owner = DB.get_user_by_carduid(carduid)

    if owner:
        print "Known user"
        continue

    n = raw_input("Type the mail associated to this card:")
    print "Will use: " + str(n)
    
    DB.add_user(n, "nope", "nope", int("False" != 'False'), str(carduid))

    print "Done, next card, please."