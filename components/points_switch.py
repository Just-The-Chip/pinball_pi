from comm.constants import COMM_LIGHTS
from comm.util import build_light_message, build_light_off_message
from components.util import HandlerResponse


class PointsSwitch:
    def __init__(self, **kwargs) -> None:
        self.base_points: int = kwargs.pop("points_value", 5)
        self.light_group_id: int | None = kwargs.pop("light_group_id", None)
        self.pattern_id: int = kwargs.pop("pattern_id", 1)
        self.pattern_option: int = kwargs.pop("pattern_option", 0)
        self.variant_id: int = kwargs.pop("variant_id", 0)
        self.should_cycle_variants: bool = kwargs.pop("should_cycle_variants", True)
        self.max_variants: int = kwargs.pop("max_variants", 4)
        self.sound: str = kwargs.pop("sound", None) # string representing the sound or sound group of the component

    def handle_message(self, msg, gameState):
        gameState.add_points(self.base_points)

        result_messages = []
        if self.has_light_group():
            result_messages.append((COMM_LIGHTS, self.build_flash_message()))

            if self.should_cycle_variants:
                self.cycle_variants()

        if self.sound == None:
            sounds_array = None
        else:
            sounds_array = [self.sound]

        return HandlerResponse(messages=result_messages, sounds=sounds_array)

    def cycle_variants(self):
        max_variant_id = self.max_variants - 1
        self.variant_id = self.variant_id + 1 if self.variant_id < max_variant_id else 0

    def has_light_group(self):
        return self.light_group_id is not None

    def build_flash_message(self):
        return build_light_message(self.light_group_id, self.pattern_id, self.variant_id, self.pattern_option)

    def reset_lights(self, _gameState):
        if self.has_light_group():
            return HandlerResponse(messages=[(COMM_LIGHTS, build_light_off_message(self.light_group_id))])

        return HandlerResponse()
