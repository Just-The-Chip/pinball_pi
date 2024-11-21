from comm.constants import COMM_SERVOS, COMM_SOLENOIDS, COMM_LIGHTS
from comm.util import build_component_message, build_light_message, build_light_error_message, build_light_off_message
from components.state_switch import StateSwitch

# at some point I will refactor out the target state stuff into its own base class


class MagBridge:
    targets = {}

    def __init__(self, **kwargs) -> None:
        self.rejector_id = kwargs.pop("rejector_id")
        self.mag_bridge_id = kwargs.pop("mag_bridge_id")
        self.state_group = kwargs.pop("state_group")

        self.ball_catch_light_group = kwargs.pop("ball_catch_light_group", None)
        self.ball_catch_pattern_id = kwargs.pop("ball_catch_pattern_id", 2)
        self.ball_catch_variant_id = kwargs.pop("ball_catch_variant_id", 2)

        target_points = kwargs.pop("target_points", 0)
        self.build_targets(kwargs.pop("target_settings"), target_points)

    def build_targets(self, target_settings, target_points):
        for target in target_settings:
            target_id = target["component_id"]
            light_group_id = target["light_group_id"]
            self.targets[target_id] = StateSwitch(
                state_key=(self.state_group, target_id),
                toggle=False,
                points_value=target_points,
                light_group_id=light_group_id
            )

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
        result_queue = []
        for target_id, target in self.targets.items():
            gameState.set_state((self.state_group, target_id), False)
            result_queue.extend(target.build_light_message(gameState))

        return result_queue

    def handle_state(self, gameState):
        state_val = self.is_group_fully_triggered(gameState)
        gameState.set_state("mag_bridge_is_active", state_val)

        if (gameState.has_state_changed("mag_bridge_is_active", False) or
                gameState.has_state_changed("mag_bridge_error", False)):
            print("OMG ITS GAME TIME................................")

            return self.build_light_message(gameState)

        return []

    def handle_mag_bridge_message(self, message, gameState):
        result_queue = []
        if message > 0:
            result_queue = self.reset_state_group(gameState)
            gameState.set_state("mag_bridge_is_traveling", False)
            print("--Mag bridge has reset")
        else:
            gameState.set_state("mag_bridge_error", True)
            print("MAG BRIDGE ERROR! OH NO!!!!!!!!!!!!!")

        return result_queue

    def handle_sensor_message(self, message, gameState):
        if message > 0 and not gameState.get_state("mag_bridge_is_traveling", False):
            state_val = gameState.get_state("mag_bridge_is_active", False)
            print(f"Mag bridge {str(self.state_group)} started! State: {str(state_val)}")

            if state_val:
                return self.trigger_bridge(gameState)
            else:
                return self.reject_ball(gameState)
        else:
            if gameState.get_state("mag_bridge_error", False):
                print("The mag bridge has errored out. Restart to attempt to fix it.")
            else:
                print("the mag bridge is not reADY YETTTTT!!!!!")

        return []  # once lights is hooked up we can add message to send to lights

    def reject_ball(self, gameState):
        return [(COMM_SOLENOIDS, build_component_message(self.rejector_id))]

    def trigger_bridge(self, gameState):
        gameState.set_state("mag_bridge_is_traveling", True)
        return [(COMM_SERVOS, build_component_message(self.mag_bridge_id))]

    def build_light_message(self, gameState):
        if self.ball_catch_light_group is None:
            return []

        light_message = build_light_off_message(self.ball_catch_light_group)

        if gameState.get_state("mag_bridge_error", False) is True:
            light_message = build_light_error_message(self.ball_catch_light_group)

        elif gameState.get_state("mag_bridge_is_active", False) is True:
            pattern_id = self.ball_catch_pattern_id
            variant_id = self.ball_catch_variant_id
            light_message = build_light_message(self.ball_catch_light_group, pattern_id, variant_id)

        return [(COMM_LIGHTS, light_message)]
