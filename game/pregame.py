from time import time
from typing import List
from .screen import Screen
from .score_repository import ScoreRecord

START_GAME_DISPLAY = 0
HIGH_SCORE_DISPLAY = 1

START_GAME_TIME_MS = 8000
HIGH_SCORE_TIME_MS = 15000

START_GAME_SCROLL_SPEED = 1
HIGH_SCORE_SCROLL_SPEED = 0.35


class PreGame:

    def __init__(self, start_button_id, comm_handler, screen: Screen) -> None:
        self.comm_handler = comm_handler
        self.start_button_id = start_button_id
        self.screen: Screen = screen
        self.game_in_progress = False
        self.log_messages = False
        self.screen_mode = START_GAME_DISPLAY
        self.start_game_start_time = 0
        self.high_score_start_time = 0

    def resume(self, top_scores: List[ScoreRecord]):
        self.game_in_progress = False
        self.screen.set_mode(3)
        self.screen.set_scroll_speed(HIGH_SCORE_SCROLL_SPEED)
        self.screen.set_top_scores(top_scores)
        self.screen_mode = HIGH_SCORE_DISPLAY
        self.start_game_start_time = 0
        self.high_score_start_time = 0

    def loop(self):
        while not self.game_in_progress:
            self.handle_incoming_messages()
            self.update_screen()

    # 00000000  0000 0000
    # ---id---  ---msg---
    def handle_incoming_messages(self):
        messages = self.comm_handler.read_all()

        # self.printMsg(f"message count: {len(messages)}")
        for id_message in messages:
            int_message = int.from_bytes(id_message, byteorder="big")
            id = (int_message >> 8)

            self.printMsg(f"MESSAGE ID: {str(id)}")

            if id == self.start_button_id:
                self.printMsg("GAME STARTED!!!!!!!!!", True)
                self.game_in_progress = True

            else:
                idString = str(id)
                self.printMsg(f"component id not found: {idString}", (len(idString) > 3))

    def update_screen(self):
        if self.screen_mode == START_GAME_DISPLAY:
            self.update_game_start_display()
        elif self.screen_mode == HIGH_SCORE_DISPLAY:
            self.update_high_score_display()

    def update_game_start_display(self):
        if self.start_game_start_time == 0:
            self.start_game_start_time = time() * 1000
        elif (time() * 1000) - self.start_game_start_time >= START_GAME_TIME_MS:
            self.screen_mode = HIGH_SCORE_DISPLAY
            self.screen.set_mode(3)  # high score mode
            self.screen.set_scroll_speed(HIGH_SCORE_SCROLL_SPEED)
            self.start_game_start_time = 0

        self.screen.set_display_text("START GAME! (>^ ^)> o")
        self.screen.update()

    def update_high_score_display(self):
        if self.high_score_start_time == 0:
            self.high_score_start_time = time() * 1000
        elif (time() * 1000) - self.high_score_start_time >= HIGH_SCORE_TIME_MS:
            self.screen_mode = START_GAME_DISPLAY
            self.screen.set_mode(0)
            self.screen.set_scroll_speed(START_GAME_SCROLL_SPEED)
            self.high_score_start_time = 0

        # self.screen.high_score_update()
        self.screen.update()

    def printMsg(self, message, force=False):
        if self.log_messages or force:
            print(message)
