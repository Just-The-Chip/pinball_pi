from comm.constants import COMM_LIGHTS
from comm.util import build_light_message, build_light_off_message


class PointsSwitch:
    def __init__(self, **kwargs) -> None:
        self.base_points = kwargs.pop("points_value", 5)
        self.light_group_id = kwargs.pop("light_group_id", None)
        self.pattern_id = kwargs.pop("pattern_id", 1)
        self.pattern_option = kwargs.pop("pattern_option", 0)

        # this implementation does kind of require the python code to know w
        self.variant_id = 0  # for now nothing fancy, just a simple flash

    def handle_message(self, msg, gameState):
        gameState.add_points(self.base_points)

        result_messages = []
        if self.has_light_group():
            result_messages.append((COMM_LIGHTS, self.build_flash_message()))
            # temp behavior because flash pattern ain't ready yet
            self.variant_id = self.variant_id + 1 if self.variant_id < 3 else 0

        return result_messages

    def has_light_group(self):
        return self.light_group_id is not None

    def build_flash_message(self):
        return build_light_message(self.light_group_id, self.pattern_id, self.variant_id, self.pattern_option)

    def reset_lights(self, _gameState):
        if self.has_light_group():
            return [(COMM_LIGHTS, build_light_off_message(self.light_group_id))]

        return []
