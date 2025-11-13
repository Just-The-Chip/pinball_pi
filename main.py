#!/usr/bin/env python3
from rgbmatrix import graphics
from game.game import Game
from game.pregame import PreGame
from game.screen import Screen
from config.init.drop_targets import init_multiball
from config.init.pop_bumpers import init_pop_bumpers
from config.init.mag_bridge import init_mag_bridge
from config.init.plinko import init_plinko
from config.init.slider import init_slider
from config.init.startup import init_startup
from config.init.rollovers import init_rollovers
from config.init.left_launcher import init_left_launcher
from comm.base_comm import BaseComm
from comm.comm_handler import CommHandler
from comm.constants import COMM_SERVOS, COMM_LIGHTS, COMM_SOLENOIDS, COMM_SOLENOIDS2
from data.constants import IS_PLINKO_ACTIVE
from player import Player
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
        COMM_SOLENOIDS, BaseComm(name=COMM_SOLENOIDS, port="/dev/ttyACM_ARDUINO3", message_size=3))
    comm_handler.register_comm(
        COMM_SOLENOIDS2, BaseComm(name=COMM_SOLENOIDS2, port="/dev/ttyACM_ARDUINO4", message_size=3))
    comm_handler.register_comm(
        COMM_SERVOS, BaseComm(name=COMM_SERVOS, port="/dev/ttyACM_ARDUINO1", message_size=3))
    comm_handler.register_comm(
        COMM_LIGHTS, BaseComm(name=COMM_LIGHTS, port="/dev/ttyACM_ARDUINO2", message_size=3))
    player = Player()

    font = graphics.Font()
    font.LoadFont("../rpi-rgb-led-matrix/fonts/6x10.bdf")
    multiplier_font = graphics.Font()
    multiplier_font.LoadFont("../rpi-rgb-led-matrix/fonts/5x8.bdf")

    screen = Screen(font=font, multiplier_font=multiplier_font)

    pregame = PreGame(2, comm_handler, screen)
    game = Game(comm_handler, screen, player)

    init_startup(game)
    init_rollovers(game)
    init_pop_bumpers(game)
    init_multiball(game)
    init_mag_bridge(game)
    init_plinko(game)
    init_slider(game)
    init_left_launcher(game)

    while True:
        pregame.resume()
        pregame.loop()

        game.start()
        game.loop()
        game.end()

        # later a post game object will take the state from the game and save high scores.
