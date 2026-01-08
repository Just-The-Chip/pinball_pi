import math
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
import sys
import os
import random
from typing import List
from .score_repository import ScoreRecord

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

HIGH_SCORE_PAUSE_TIME_MS = 2000
BLINK_INTERVAL_MS = 250


class Screen(object):
    def __init__(self, *args, **kwargs):
        self.font = kwargs.get("font")
        self.multiplier_font = kwargs.get("multiplier_font")
        self.multiplier_color = graphics.Color(255, 64, 10)

        self.set_random_text_color()

        self.args = {}
        self.args["rows"] = kwargs.get("rows", 32)
        self.args["cols"] = kwargs.get("cols", 64)
        self.args["chain_length"] = kwargs.get("chain_length", 1)
        self.args["brightness"] = kwargs.get("brightness", 100)
        self.setup_matrix()

        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.display_score = 0
        self.multiplier = 1
        self.balls_remaining = 0
        self.last_canvas_update = 0
        self.screen_mode = 0  # 0 = pregame, 1 = game, -1 = postgame
        self.scroll_speed = 1
        self.vertical_scroll_speed = 1

        self.current_name = []
        self.name_position_index = 0

        self.pregame_text_pos = self.offscreen_canvas.width
        self.top_scores: List[ScoreRecord] = []
        self.high_score_text_offset = 0
        self.high_score_pause_time = 0

    def set_mode(self, mode):
        if mode > 3 or mode < 0:
            self.screen_mode = 0
        else:
            self.screen_mode = mode

        if self.screen_mode == 0:
            self.set_random_text_color()
            self.pregame_text_pos = self.offscreen_canvas.width
        elif self.screen_mode == 2:
            self.current_name = ["_"] * 3
            self.name_position_index = 0
        elif self.screen_mode == 3:
            self.set_random_text_color()
            self.high_score_text_offset = 0
            self.high_score_pause_start_time = 0

    def set_random_text_color(self):
        random_red = random.randrange(0, 255)
        random_green = random.randrange(0, 255)
        random_blue = random.randrange(0, 255)

        self.set_text_color(r=random_red, g=random_green, b=random_blue)

    def set_text_color(self, **kwargs):
        self.text_color = graphics.Color(kwargs["r"], kwargs["g"], kwargs["b"])

    def set_display_score(self, score):
        if score != self.display_score:
            self.set_random_text_color()

        self.display_score = score

    def set_name_data(self, name_position_index, entered_name):
        self.name_position_index = name_position_index
        self.current_name = entered_name

    def set_top_scores(self, top_scores: List[ScoreRecord]):
        self.top_scores = top_scores

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier

    def set_balls_remaining(self, balls_remaining):
        self.balls_remaining = balls_remaining

    def set_display_text(self, text):
        self.display_text = text

    def set_scroll_speed(self, speed):
        self.scroll_speed = speed

    def setup_matrix(self):
        options = RGBMatrixOptions()

        options.hardware_mapping = "adafruit-hat-pwm"
        options.rows = self.args.get("rows")
        options.cols = self.args.get("cols")
        options.chain_length = self.args.get("chain_length")
        options.parallel = 1
        options.brightness = self.args.get("brightness")
        options.gpio_slowdown = 4

        self.matrix = RGBMatrix(options=options)

    def scroll_text_update(self):
        length = graphics.DrawText(self.offscreen_canvas, self.font,
                                   self.pregame_text_pos, 15, self.text_color, self.display_text)

        self.pregame_text_pos -= self.scroll_speed

        if self.pregame_text_pos + length < 0:
            self.set_random_text_color()
            self.pregame_text_pos = self.offscreen_canvas.width

    def high_score_update(self):
        rounded_offset = round(self.high_score_text_offset)

        graphics.DrawText(self.offscreen_canvas, self.font,
                          2, 7 + rounded_offset, self.multiplier_color, "The Champs")

        y_pos = 16
        for record in self.top_scores:
            score_text = f"{record['player'].ljust(4, ' ')} {str(record['score']).rjust(7, ' ')}"

            graphics.DrawText(self.offscreen_canvas, self.multiplier_font,
                              2, y_pos + rounded_offset, self.text_color, score_text)
            y_pos += 8

        if self.high_score_text_offset == 0:
            if self.high_score_pause_start_time == 0:
                self.high_score_pause_start_time = time.time() * 1000

            if (time.time() * 1000) - self.high_score_pause_start_time >= HIGH_SCORE_PAUSE_TIME_MS:
                self.high_score_pause_start_time = 0
            else:
                return

        self.high_score_text_offset -= self.scroll_speed

    def game_update(self):
        graphics.DrawText(self.offscreen_canvas, self.font,
                          2, 10, self.text_color, str(self.display_score))

        bottom_text = f"x{str(self.multiplier)}  Ball: {str(self.balls_remaining)}"
        graphics.DrawText(self.offscreen_canvas, self.multiplier_font,
                          2, 30, self.multiplier_color, bottom_text)

    def name_input_update(self):
        is_cursor_visible = math.floor(time.time() * 1000 / BLINK_INTERVAL_MS) % 2 == 0

        display_name = ""
        for index, letter in enumerate(self.current_name):
            if is_cursor_visible and index == self.name_position_index:
                display_name += "_" if letter != "_" else " "
            else:
                display_name += letter

        graphics.DrawText(self.offscreen_canvas, self.multiplier_font,
                          2, 10, self.text_color, f"Enter Name:")

        graphics.DrawText(self.offscreen_canvas, self.font,
                          2, 25, self.text_color, display_name)

    def update(self):
        current_time = time.time() * 1000
        if current_time >= self.last_canvas_update + 50:
            self.offscreen_canvas = self.matrix.SwapOnVSync(
                self.offscreen_canvas)
            self.last_canvas_update = current_time
            self.offscreen_canvas.Clear()

            # start prompt, final (later)
            if self.screen_mode == 0:
                self.scroll_text_update()

            # current score
            if self.screen_mode == 1:
                self.game_update()

            if self.screen_mode == 2:
                self.name_input_update()

            if self.screen_mode == 3:
                self.high_score_update()
