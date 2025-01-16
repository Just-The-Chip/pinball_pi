from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))


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
        self.last_canvas_update = 0

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

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier

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

    def update(self):
        current_time = time.time() * 1000
        if current_time >= self.last_canvas_update + 50:
            self.offscreen_canvas = self.matrix.SwapOnVSync(
                self.offscreen_canvas)
            self.last_canvas_update = current_time

            self.offscreen_canvas.Clear()
            graphics.DrawText(self.offscreen_canvas, self.font,
                              2, 10, self.text_color, str(self.display_score))
            graphics.DrawText(self.offscreen_canvas, self.multiplier_font,
                              2, 30, self.multiplier_color, f"x{str(self.multiplier)}")
