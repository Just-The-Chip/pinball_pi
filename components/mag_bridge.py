from comm.constants import COMM_SERVOS, COMM_SOLENOIDS, COMM_LIGHTS
from comm.util import build_component_message, build_light_message, build_light_error_message, build_light_off_message
from data.constants import IS_PLINKO_ACTIVE, MAG_BRIDGE_ERROR_KEY, MAG_BRIDGE_TRAVELING_KEY

# at some point I will refactor out the target state stuff into its own base class


class MagBridge:
    def __init__(self, **kwargs) -> None:
        self.rejector_id = kwargs.pop("rejector_id")
        self.mag_bridge_id = kwargs.pop("mag_bridge_id")
        self.switch_group = kwargs.pop("switch_group")
        # self.state_group = kwargs.pop("state_group")

        self.ball_catch_light_group = kwargs.pop("ball_catch_light_group", None)
        self.ball_catch_pattern_id = kwargs.pop("ball_catch_pattern_id", 2)
        self.ball_catch_variant_id = kwargs.pop("ball_catch_variant_id", 2)

        self.is_active_key = "mag_bridge_is_active"
        self.is_traveling_key = MAG_BRIDGE_TRAVELING_KEY

    def handle_state(self, gameState):
        state_val = self.switch_group.is_group_fully_triggered(gameState)
        gameState.set_state(self.is_active_key, state_val)

        if (gameState.has_state_changed(self.is_active_key, False) or
                gameState.has_state_changed(MAG_BRIDGE_ERROR_KEY, False)):
            print("OMG ITS GAME TIME................................")

            return self.build_light_message(gameState)

        return []

    def handle_cleanup(self, gameState):
        # maybe later ensure mag bridge is reset?
        print("CLEANING UP MAG BRIDGE")
        result_queue = self.switch_group.reset_state_group(gameState)
        result_queue.append((COMM_LIGHTS, build_light_off_message(self.ball_catch_light_group)))

        return result_queue

    def handle_mag_bridge_message(self, message, gameState):
        result_queue = []
        if message > 0:
            result_queue = self.switch_group.reset_state_group(gameState)
            gameState.set_state(self.is_traveling_key, False)
            print("--Mag bridge has reset")
        else:
            gameState.set_state(MAG_BRIDGE_ERROR_KEY, True)
            print("MAG BRIDGE ERROR! OH NO!!!!!!!!!!!!!")

        return result_queue

    def handle_sensor_message(self, message, gameState):
        is_traveling = gameState.get_state(self.is_traveling_key, False)
        is_plinko = gameState.get_state(IS_PLINKO_ACTIVE, False)

        if message > 0 and not is_traveling and not is_plinko:
            state_val = gameState.get_state(self.is_active_key, False)
            print(f"Mag bridge sensor hit! State: {str(state_val)}")

            if state_val:
                gameState.set_state(IS_PLINKO_ACTIVE, True)
            else:
                return self.reject_ball(gameState)
        else:
            if gameState.get_state(MAG_BRIDGE_ERROR_KEY, False):
                print("The mag bridge has errored out. Restart to attempt to fix it.")
            else:
                print("the mag bridge is not reADY YETTTTT!!!!!")

        return []  # once lights is hooked up we can add message to send to lights

    def handle_plinko_complete(self, gameState):
        is_plinko = gameState.get_state_change(IS_PLINKO_ACTIVE, False)

        if is_plinko["from"] == True and is_plinko["to"] == False:
            print(f"Mag bridge started!")

            if gameState.get_state(MAG_BRIDGE_ERROR_KEY, False):
                print("The mag bridge has errored out. Restart to attempt to fix it.")
            else:
                return self.trigger_bridge(gameState)

        return []

    def reject_ball(self, gameState):
        return [(COMM_SOLENOIDS, build_component_message(self.rejector_id))]

    def trigger_bridge(self, gameState):
        gameState.set_state(self.is_traveling_key, True)
        return [(COMM_SERVOS, build_component_message(self.mag_bridge_id))]

    def build_light_message(self, gameState):
        if self.ball_catch_light_group is None:
            return []

        light_message = build_light_off_message(self.ball_catch_light_group)

        if gameState.get_state(MAG_BRIDGE_ERROR_KEY, False) is True:
            light_message = build_light_error_message(self.ball_catch_light_group)

        elif gameState.get_state(self.is_active_key, False) is True:
            pattern_id = self.ball_catch_pattern_id
            variant_id = self.ball_catch_variant_id
            light_message = build_light_message(self.ball_catch_light_group, pattern_id, variant_id)

        return [(COMM_LIGHTS, light_message)]
