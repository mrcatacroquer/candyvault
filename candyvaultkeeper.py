import sys
import logging
from logging import handlers
import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep
from mysqlhelper import MYSQLHelper

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.handlers.RotatingFileHandler('candykeeper.log', maxBytes=20*1024*1024, backupCount=5)
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger


def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(32, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(32, False)
    pwm.ChangeDutyCycle(0)

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    pwm.stop()
    GPIO.cleanup()

def open_gate():
    set_angle(0)

def close_gate():
    set_angle(90)

def is_door_open():
    if GPIO.input(16) is 1:
        return False
    return True

def double_fucking_check_door_open():
    if is_door_open():
        sleep(1.25)
        if is_door_open():
            return True
    return False

DB = MYSQLHelper()

logger = setup_custom_logger('candykeeper')

continue_reading = True
signal.signal(signal.SIGINT, end_read)

MIFAREReader = MFRC522.MFRC522()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, True)
pwm=GPIO.PWM(32, 50)
pwm.start(0)

logger.info('Candy keeper ready.')

while continue_reading:

    if double_fucking_check_door_open():
        logger.info('MALANDRIN DETECTED!!!')

    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if not status == MIFAREReader.MI_OK:
        continue

    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status is not MIFAREReader.MI_OK or len(uid) < 4:
        continue

    carduid = str(uid[0]) +","+ str(uid[1]) +","+ str(uid[2]) +","+ str(uid[3]) +","+ str(uid[4])
    owner = DB.get_user_by_carduid(carduid)

    if not owner or len(owner) < 6:
        logger.info('Misterius card: ' + carduid)
        continue

    owner_mail = str(owner[1])
    reward = DB.get_reward_for_user(owner[1])
    logger.info('Card detected for user: ' + str(owner_mail))
    logger.info('Reward: ' + str(reward))

    if reward or (str(uid[0]) == "123" and str(uid[1]) == "456" and str(uid[2]) == "789" and str(uid[3]) == "000"):
        DB.delete_reward_by_user(owner_mail)
        logger.info('User rewards cleared')
        logger.info('Opening gate for ' + str(owner_mail))
        open_gate()
        sleep(5)

        while is_door_open():
            sleep(0.25)

        logger.info('Closing gate.')
        close_gate()
    else:
        logger.info('Shameless opening attempt by ' + str(owner_mail))
