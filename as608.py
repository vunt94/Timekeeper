
import requests
# uart/serial protocol library
import serial
# library behavior of fingerpint from adafruit
import adafruit_fingerprint
# time
import time
from datetime import datetime
# timezone
import pytz
# Control io
import RPi.GPIO as GPIO
# check network connect
import http.client as httplib

# setup GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
   
GPIO.output(19, 1)
GPIO.output(13, 1)

uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

url = 'https://api.ms-hrms.software/human-resources-management-system/time-check'


def update_text(text):
    label.value = text


def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        time.sleep(1)
        pass
    time.sleep(1)
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        print("Finger not match")
        # GPIO.output(19, 1)
        # time.sleep(2)
        # GPIO.output(19, 0)
        return False
    return True


# pylint: disable=too-many-branches
def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="")
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False

    print("Templating...", end="")
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    print("Searching...", end="")
    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
        else:
            print("Other error")
        return False


# pylint: disable=too-many-statements
def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True


##################################################


def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = int(input("Enter ID # from 1-127: "))
        except ValueError:
            pass
    return i


def get_current_finger_print_index():
    f = open("config_finger_print.txt", "r")
    return int(f.read())


def update_index(index):
    f = open("config_finger_print.txt", "w")
    f.write(str(index))
    f.close()


def setup():
    current_index_id = get_current_finger_print_index()
    GPIO.output(19, 0)
    GPIO.output(13, 0)
    return current_index_id

# check connection ping to gg
def is_connected_to_internet():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()

# lost connect behavior
def lost_connection_action():
    while True:
        GPIO.output(19, 1)
        GPIO.output(13, 0)
        time.sleep(1)
        GPIO.output(19, 0)
        GPIO.output(13, 1)
        time.sleep(1)


def is_connected_to_server():
    pass


def main():
    status = False
    on_register = False
    register_timeout = 0
    current_index_id = setup()
    if is_connected_to_internet():
        while True:
            if on_register == False:
                if GPIO.input(26) == GPIO.HIGH and status == False:
                    print("Registering...")
                    status = True
                    on_register = True
                else:
                    if GPIO.input(26) == GPIO.LOW:
                        status = False
                if finger.read_templates() != adafruit_fingerprint.OK:
                    raise RuntimeError("Failed to read templates")
                if get_fingerprint():
                    GPIO.output(13, 1)
                    tz_NY = pytz.timezone('Asia/Bangkok')
                    now = datetime.now(tz_NY)
                    myobj = {
                        "id_signature": finger.finger_id,
                        "time_log": now.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    resp = requests.post(url, json=myobj)
                    print(resp.text)
                    print(resp.elapsed.total_seconds())
                    time.sleep(4)
                    GPIO.output(13, 0)
                else:
                    print("Finger not found")
            else:
                if register_timeout < 20:
                    register_timeout += 1
                    GPIO.output(19, 1)
                    GPIO.output(13, 1)
                    if enroll_finger(current_index_id) == True:
                        on_register = False
                        current_index_id += 1
                        update_index(current_index_id)
                        print(current_index_id)
                        time.sleep(2)
                        GPIO.output(19, 0)
                        GPIO.output(13, 0)

                else:
                    on_register = False
                    time.sleep(2)
                    GPIO.output(19, 0)
                    GPIO.output(13, 0)
    else:
        lost_connection_action()


if __name__ == "__main__":
    main()
