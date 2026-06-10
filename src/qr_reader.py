import sys
import os
import time

#sys.path.append("../")
# https://github.com/DFRobot/DFRobot_HuskylensV2/tree/master -> biblioteca
sys.path.append("/home/pi/catkin_ws/src/huskylens_2/scripts/DFRobot_HuskylensV2/python/smbus2/")
from dfrobot_huskylensv2 import *

ALGORITHM = ALGORITHM_QRCODE_RECOGNITION

huskylens = HuskylensV2_I2C()
huskylens.knock()
huskylens.switchAlgorithm(ALGORITHM)

print("QR Code Reader initializing...")

while True:
    huskylens.getResult(ALGORITHM)

    if huskylens.available(ALGORITHM):
        result = huskylens.getCachedCenterResult(ALGORITHM)
        qr_id = result.ID

        print(f"QR Code detect! ID: {qr_id}")

        # ID
        if qr_id == 1:
            print("ID 1 FOUND")
        elif qr_id == 2:
            print("ID 2 FOUND")
        else:
            print(f"(ID {qr_id})")

    time.sleep(0.1)