from comm.constants import COMM_LIGHTS
from comm.util import build_light_message, build_light_off_message


class SimpleStateIndicator:
    def __init__(self, **kwargs) -> None:
        self.light_group_id = kwargs.pop("light_group_id")
        self.indicator_key = kwargs.pop("indicator_key")
        self.pattern_id = kwargs.pop("pattern_id", 2)
        self.variant_id = kwargs.pop("variant_id", 3)
        self.pattern_option = kwargs.pop("pattern_option", 0)
        self.state_callback = kwargs.pop("state_callback")

    def handle_state(self, gameState):
        state_value = self.state_callback(gameState)
        indicator_status = gameState.get_state(self.indicator_key, False)

        if indicator_status == False and state_value == True:
            return self.turn_on_indicator(gameState)

        if indicator_status == True and state_value == False:
            return self.turn_off_indicator()

        return []

    def turn_on_indicator(self, gameState):
        gameState.set_state(self.indicator_key, True)
        return [(COMM_LIGHTS, build_light_message(
            self.light_group_id,
            self.pattern_id,
            self.variant_id,
            self.pattern_option
        ))]

    def turn_off_indicator(self, gameState):
        gameState.set_state(self.indicator_key, False)
        return [(COMM_LIGHTS, build_light_off_message(self.light_group_id))]

    def handle_cleanup(self, gameState):
        return self.turn_off_indicator(gameState)
