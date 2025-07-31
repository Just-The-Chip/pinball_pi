# from math import round
from comm.constants import COMM_LIGHTS
from comm.util import build_light_message
from time import time


# min? 20 or 28
# max? 643 or 645
# 558 top most light?
# 125 start val?
class Slider:
    def __init__(self, **kwargs) -> None:
        self.base_points = kwargs.pop("base_points_value", 0)

        # state key should be either a string for a root value or a tuple for nested values
        self.slider_timeout = 600
        self.light_group_id = kwargs.pop("light_group_id", None)
        self.end_pattern_id = kwargs.pop("end_pattern_id", 4)
        self.slider_pattern_id = kwargs.pop("slider_pattern_id", 5)
        self.slider_variant_id = kwargs.pop("slider_variant_id", 0)
        self.log_messages = False

    def handle_message(self, message, gameState):
        # message will be from 0 to 100 as a percetnt of slider plus 100
        self.printMsg(f"Slider fired! Message: {str(message)}")
        slider_percent = message - 100
        if slider_percent > 0:
            # self.printMsg(f"Slider fired! Message: {str(message)}")

            # this code will need to divide that by 7 to decide how many lights and points
            progress = round(slider_percent / 100 * 7)
            old_state = gameState.get_state("slider_progress", 0)

            if progress >= old_state and progress > 0:
                self.printMsg(f"Slider progress: {str(progress)}")
                gameState.set_state("slider_progress", progress)
                gameState.set_state("slider_timestamp", time() * 1000)

                if progress > old_state:
                    return self.build_light_message(progress)
        return []

    def handle_state(self, gameState):

        slider_timestamp = gameState.get_state("slider_timestamp", 0)
        now = time() * 1000

        if slider_timestamp > 0 and (now - slider_timestamp) >= self.slider_timeout:
            final_progress = gameState.get_state("slider_progress", 0)

            self.printMsg(f"Final progress: {str(final_progress)}")

            gameState.set_state("slider_progress", 0)
            gameState.set_state("slider_timestamp", 0)
            gameState.add_points(self.calculate_points(final_progress))

            return self.build_end_light_message(final_progress)
        return []

    def calculate_points(self, progress):
        # this might be too disproportionate but we can change it later if necessary
        return self.base_points * (2 ** (progress - 1))

    def build_end_light_message(self, progress):
        if self.light_group_id is not None:
            pattern_id = self.end_pattern_id if progress else 0
            variant_id = progress - 1 if progress else 0
            return [(COMM_LIGHTS, build_light_message(self.light_group_id, pattern_id, variant_id, progress))]

        return []

    def build_light_message(self, progress):
        if self.light_group_id is not None:
            pattern_id = self.slider_pattern_id
            variant_id = self.slider_variant_id
            return [(COMM_LIGHTS, build_light_message(self.light_group_id, pattern_id, variant_id, progress - 1))]

        return []

    def printMsg(self, message):
        if self.log_messages:
            print(message)
