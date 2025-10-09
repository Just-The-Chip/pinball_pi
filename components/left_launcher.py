from comm.constants import COMM_SOLENOIDS2
from comm.util import build_component_message
from components.state_switch_group import StateSwitchGroup
from components.util import HandlerResponse
from time import time


class LaneSwitchHandler:
    def __init__(self, **kwargs) -> None:
        self.switch_group: StateSwitchGroup = kwargs.pop("switch_group")
        self.door_state_key = kwargs.pop("door_state_key")
        self.left_flipper_id: int = kwargs.pop("left_flipper_id")
        self.right_flipper_id: int = kwargs.pop("right_flipper_id")

    def register_handlers(self, game):
        game.register_startup_handler(self.switch_group.reset_state_group)
        self.switch_group.register_message_handlers(game)

        game.register_message_handler(self.left_flipper_id, self.left_flipper_handler)
        game.register_message_handler(self.right_flipper_id, self.right_flipper_handler)
        game.register_state_handler(self.handle_state)

    def left_flipper_handler(self, message, gameState):
        return self.switch_group.shift_state_group(gameState, True)

    def right_flipper_handler(self, message, gameState):
        return self.switch_group.shift_state_group(gameState, False)

    def handle_state(self, gameState):
        diff = gameState.get_state_change(self.door_state_key, False)

        # this handler can turn on the door flag, but something else will turn it off
        if diff["to"] == False and diff["from"] == True:
            return self.switch_group.reset_state_group(gameState)

        fully_triggered = self.switch_group.is_group_fully_triggered(gameState)

        # if something else opened the door, all switches should automaticaly turn active
        if diff["to"] == True and diff["from"] == False and not fully_triggered:
            return self.switch_group.activate_state_group(gameState)

        # activating all four switches is one of the ways to open the door
        if fully_triggered and diff["to"] == False:
            gameState.set_state(self.door_state_key, True)

        return HandlerResponse()


class LeftLauncher:
    def __init__(self, **kwargs) -> None:
        self.door_state_key = kwargs.pop("door_state_key")
        self.launcher_id: int = kwargs.pop("launcher_id")

        self.launcher_pause_time = 2000
        self.launcher_pause_key = "left_launcher_pause_time"
        self.launch_key = "left_launcher_activated"

    def handle_left_lane_rollover(self, message, gameState):
        print("IMPORTANT MESSAGE FROM LEFT LANE OVERLORD")

        if gameState.get_state(self.launch_key, False):
            gameState.set_state(self.launch_key, False)
            gameState.set_state(self.door_state_key, False)

        elif gameState.get_state(self.door_state_key, False):
            gameState.set_state(self.launcher_pause_key, time() * 1000)

        return HandlerResponse()

    def handle_state(self, gameState):
        pause_start = gameState.get_state(self.launcher_pause_key, 0)
        is_launched = gameState.get_state(self.launch_key, False)

        if not is_launched and pause_start > 0 and time() * 1000 >= pause_start + self.launcher_pause_time:
            print("FJDKSFJSKF LAUNCHE THE BAAAAALLLLLLLL")
            gameState.set_state(self.launcher_pause_key, 0)
            gameState.set_state(self.launch_key, True)
            return HandlerResponse(messages=[(COMM_SOLENOIDS2, build_component_message(self.launcher_id))])

        return HandlerResponse()
