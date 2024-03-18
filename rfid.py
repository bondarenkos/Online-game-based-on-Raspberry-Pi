#!/usr/bin/env python3

# pylint: disable=no-member

import time
import RPi.GPIO as GPIO
from config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522

def rfidRead():
    (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
    if status == self.MIFAREReader.MI_OK:
        (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
        if status == self.MIFAREReader.MI_OK:
            num = 0
            for i in range(0, len(uid)):
                num += uid[i] << (i*8)
            print(f"Card read UID: {uid} > {self.num}")
            time.sleep(0.5)
            return num
    self.after(50, selfrfidRed)

def test():
    print('\nThe RFID reader test.')
    print('Place the card close to the reader (on the right side of the set).')
    rfidRead()
    print("The RFID reader tested successfully.")


if __name__ == "__main__":
    test()
    GPIO.cleanup()  # pylint: disable=no-member
