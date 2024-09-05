# from comm.constants import COMM_SERVOS
# from comm.util import build_component_message


class StateSwitch:
    def __init__(self, **kwargs) -> None:
        # self.id = kwargs.pop("id")
        # self.group_id = kwargs.pop("group_id")
        self.toggle = kwargs.pop("toggle", False)
        self.base_points = kwargs.pop("points_value", 0)

        # state key should be either a string for a root value or a tuple for nested values
        self.state_key = kwargs.pop("state_key")

    def handle_message(self, message, gameState):
        print(message)
        if message > 0:
            new_state = self.set_state(gameState)
            print(f"{str(self.state_key)} state switch fired! State: {str(new_state)}")

            if new_state:
                gameState.add_points(self.base_points)

        return []  # once lights is hooked up we can add message to send to lights

    def set_state(self, gameState):
        old_state = gameState.get_state(self.state_key, False)
        new_state = not old_state if self.toggle else True
        gameState.set_state(self.state_key, new_state)

        return new_state

# TODO: state handler to set "mag_bridge_active" to true
