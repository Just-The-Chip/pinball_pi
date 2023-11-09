#!/usr/bin/env python3
from game.game import Game
from config.init.drop_targets import init_drop_targets
from comm.base_comm import BaseComm
from comm.comm_handler import CommHandler, COMM_SERVOS, COMM_LIGHTS
import serial
import time

import sys
import os

curpath = os.path.abspath(os.path.join(__file__, os.pardir))
if (curpath not in sys.path):
    sys.path.append(curpath)


if __name__ == '__main__':
    comm_handler = CommHandler()
    comm_handler.register_comm(
        COMM_SERVOS, BaseComm(port="/dev/ttyACM_ARDUINO1"))
    comm_handler.register_comm(
        COMM_LIGHTS, BaseComm(port="/dev/ttyACM_ARDUINO2"))

    game = Game(comm_handler)

    game.start()
    game.loop()
    game.end()
