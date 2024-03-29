#!/usr/bin/env python3
from game.game import Game
from config.init.drop_targets import init_drop_targets
from config.init.pop_bumpers import init_pop_bumpers
from comm.base_comm import BaseComm
from comm.comm_handler import CommHandler
from comm.constants import COMM_SERVOS, COMM_LIGHTS, COMM_SOLENOIDS
# import serial
import time

import sys
import os

curpath = os.path.abspath(os.path.join(__file__, os.pardir))
if (curpath not in sys.path):
    sys.path.append(curpath)


if __name__ == '__main__':
    comm_handler = CommHandler()
    comm_handler.register_comm(
        COMM_SOLENOIDS, BaseComm(port="/dev/ttyACM_ARDUINO3", message_size=3))
    comm_handler.register_comm(
        COMM_SERVOS, BaseComm(port="/dev/ttyACM_ARDUINO1", message_size=3))
    # comm_handler.register_comm(
    #     COMM_LIGHTS, BaseComm(port="/dev/ttyACM_ARDUINO2", message_size=3))

    game = Game(comm_handler)

    init_pop_bumpers(game)
    init_drop_targets(game)

    game.start()
    game.loop()
    game.end()
