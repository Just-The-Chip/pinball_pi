from data.constants import LEFT_LANE_DOOR_KEY
from comm.constants import COMM_SERVOS
from components.state_switch import StateSwitch
from components.state_trigger import StateTrigger
from components.state_switch_group import StateSwitchGroup
from components.left_launcher import LaneSwitchHandler, LeftLauncher
from components.simple_state_indicator import SimpleStateIndicator

ballSaveIndicatorR = SimpleStateIndicator(
    light_group_id=22,
    pattern_id=6,
    variant_id=1,
    pattern_option=3,
    indicator_key="ball_save_indicator_r",
    state_callback=lambda gameState: gameState.is_ball_save_active()
)

ballSaveIndicatorL = SimpleStateIndicator(
    light_group_id=21,
    pattern_id=6,
    variant_id=1,
    pattern_option=3,
    indicator_key="ball_save_indicator_l",
    state_callback=lambda gameState: gameState.get_state(LEFT_LANE_DOOR_KEY, False) or gameState.is_ball_save_active()
)

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
        {"component_id": 47, "light_group_id": 24, "pattern_id": 1, "variant_id": 3},
        {"component_id": 48, "light_group_id": 25, "pattern_id": 1, "variant_id": 3},
        {"component_id": 49, "light_group_id": 26, "pattern_id": 1, "variant_id": 3},
        {"component_id": 50, "light_group_id": 27, "pattern_id": 1, "variant_id": 3}
    ),
    target_points=10
)

lane_handler = LaneSwitchHandler(
    switch_group=bottom_lane_group,
    door_state_key=LEFT_LANE_DOOR_KEY,
    left_flipper_id=52,
    right_flipper_id=53
)

left_launcher = LeftLauncher(
    door_state_key=LEFT_LANE_DOOR_KEY,
    launcher_id=54
)


def init_left_launcher(game):
    game.register_message_handler(16, top_lane_rollover.handle_message)
    lane_handler.register_handlers(game)

    game.register_state_handler(left_launcher_door.handle_state)
    game.register_cleanup_handler(left_launcher_door.untrigger_component)

    game.register_state_handler(ballSaveIndicatorR.handle_state)
    game.register_cleanup_handler(ballSaveIndicatorR.handle_cleanup)

    game.register_state_handler(ballSaveIndicatorL.handle_state)
    game.register_cleanup_handler(ballSaveIndicatorL.handle_cleanup)

    game.register_message_handler(45, left_launcher.handle_left_lane_rollover)
    game.register_state_handler(left_launcher.handle_state)
