#!/usr/bin/env python3
from comm.base_comm import BaseComm
import serial
import time

import sys
import os

curpath = os.path.abspath(os.path.join(__file__, os.pardir))
if (curpath not in sys.path):
    sys.path.append(curpath)


if __name__ == '__main__':
    comm2 = BaseComm(port="/dev/ttyACM_ARDUINO2")
    comm1 = BaseComm(port="/dev/ttyACM_ARDUINO1")

    send_interval = 2
    last_send = 0

    click_count = 0

    while True:
        messages = comm1.read_buffer()

        if len(messages) > 0:
            click_count += 1
            print(f"Click count: {click_count}")

        for message in messages:
            if message.decode("utf-8") == "one":
                comm2.write_message("two\n")
                # print("writing message")
            else:
                print(f"bad message: {message}")

        # if time.time() >= last_send + send_interval:
        #     print("sending message...")
        #     last_send = time.time()
        #     comm2.write_message("two\n")
