# from comm.constants import COMM_SERVOS
# from comm.util import build_component_message
from comm.constants import COMM_LIGHTS
from comm.util import build_light_message


class StateSwitch:
    def __init__(self, **kwargs) -> None:
        # self.id = kwargs.pop("id")
        # self.group_id = kwargs.pop("group_id")
        self.toggle = kwargs.pop("toggle", False)
        self.base_points = kwargs.pop("points_value", 0)

        # state key should be either a string for a root value or a tuple for nested values
        self.state_key = kwargs.pop("state_key")
        self.light_group_id = kwargs.pop("light_group_id", None)
        self.pattern_id = kwargs.pop("pattern_id", 2)
        self.variant_id = kwargs.pop("variant_id", 3)

    def handle_message(self, message, gameState):
        print(message)
        if message > 0:
            new_state = self.update_state(gameState)
            print(f"{str(self.state_key)} state switch fired! State: {str(new_state)}")

            if new_state:
                gameState.add_points(self.base_points)

            return self.build_light_message(gameState)

        return []  # once lights is hooked up we can add message to send to lights

    def update_state(self, gameState):
        old_state = gameState.get_state(self.state_key, False)
        new_state = not old_state if self.toggle else True
        gameState.set_state(self.state_key, new_state)

        return new_state

    def build_light_message(self, gameState):
        if self.light_group_id is not None:
            current_state = gameState.get_state(self.state_key, False)
            pattern_id = self.pattern_id if current_state else 0
            variant_id = self.variant_id if current_state else 0
            return [(COMM_LIGHTS, build_light_message(self.light_group_id, pattern_id, variant_id))]

        return []

    def activate_state(self, gameState):
        gameState.set_state(self.state_key, True)
        return self.build_light_message(gameState)

    def reset_state(self, gameState):
        gameState.set_state(self.state_key, False)
        return self.build_light_message(gameState)
