from data.constants import LEFT_LANE_DOOR_KEY
from comm.constants import COMM_SERVOS
from components.state_switch import StateSwitch
from components.state_trigger import StateTrigger
from components.state_switch_group import StateSwitchGroup

top_lane_rollover = StateSwitch(
    toggle=True,
    state_key=LEFT_LANE_DOOR_KEY
)

left_launcher_door = StateTrigger(
    target_id=51,
    comm_name=COMM_SERVOS,
    state_key=LEFT_LANE_DOOR_KEY
)

bottom_lane_group = StateSwitchGroup(
    state_group="bottom_lane_switches",
    target_settings=(
        {"component_id": 47, "light_group_id": 24},
        {"component_id": 48, "light_group_id": 25},
        {"component_id": 49, "light_group_id": 26},
        {"component_id": 50, "light_group_id": 27}
    ),
    target_points=10
)


def test_left_flipper_handler(message, gameState):
    return bottom_lane_group.shift_state_group(gameState, True)


def test_right_flipper_handler(message, gameState):
    return bottom_lane_group.shift_state_group(gameState, False)


def init_left_launcher(game):
    game.register_message_handler(16, top_lane_rollover.handle_message)
    game.register_state_handler(left_launcher_door.handle_state)
    game.register_cleanup_handler(left_launcher_door.untrigger_component)

    bottom_lane_group.register_message_handlers(game)
    game.register_startup_handler(bottom_lane_group.reset_state_group)
    game.register_message_handler(52, test_left_flipper_handler)
    game.register_message_handler(53, test_right_flipper_handler)
