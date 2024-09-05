from comm.constants import COMM_SERVOS, COMM_SOLENOIDS
from comm.util import build_component_message
from components.state_switch import StateSwitch

# at some point I will refactor out the target state stuff into its own base class


class MagBridge:
    targets = {}

    def __init__(self, **kwargs) -> None:
        self.rejector_id = kwargs.pop("rejector_id")
        self.mag_bridge_id = kwargs.pop("mag_bridge_id")
        self.state_group = kwargs.pop("state_group")

        target_points = kwargs.pop("target_points", 0)
        self.build_targets(kwargs.pop("target_ids"), target_points)

    def build_targets(self, target_ids, target_points):
        for target_id in target_ids:
            self.targets[target_id] = StateSwitch(
                state_key=(self.state_group, target_id), toggle=False, points_value=target_points)

    def register_message_handlers(self, game):
        for target_id, target in self.targets.items():
            game.register_message_handler(target_id, target.handle_message)

    def is_group_fully_triggered(self, gameState):
        state = gameState.get_state(self.state_group, {})

        total_state = True

        for target_id in self.targets:
            total_state = total_state and state.get(target_id, False)

        return total_state

    def reset_state_group(self, gameState):
        for target_id in self.targets:
            gameState.set_state((self.state_group, target_id), False)

    def handle_message(self, message, gameState):
        print(message)
        if message > 0:
            state_val = self.is_group_fully_triggered(gameState)
            print(f"Mag bridge {str(self.state_group)} fired! State: {str(state_val)}")

            if state_val:
                return self.trigger_bridge(gameState)
            else:
                return self.reject_ball(gameState)

        return []  # once lights is hooked up we can add message to send to lights

    def reject_ball(self, gameState):
        return [(COMM_SOLENOIDS, build_component_message(self.rejector_id))]

    def trigger_bridge(self, gameState):
        self.reset_state_group(gameState)
        return [(COMM_SERVOS, build_component_message(self.mag_bridge_id))]
