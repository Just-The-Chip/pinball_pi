from components.mag_bridge import MagBridge
from components.mag_bridge_spinner import MagBridgeSpinner
from components.state_switch_group import StateSwitchGroup
from components.points_switch import PointsSwitch

mag_bridge_switch_group = StateSwitchGroup(
    state_group="mag_bridge_switches",
    target_settings=(
        {"component_id": 17, "light_group_id": 6},
        {"component_id": 18, "light_group_id": 7},
        {"component_id": 19, "light_group_id": 8},
        {"component_id": 20, "light_group_id": 9}
    ),
    target_points=200
)

mag_bridge = MagBridge(
    switch_group=mag_bridge_switch_group,
    ball_catch_light_group=11,
    ball_catch_variant_id=0,
    rejector_id=22,
    mag_bridge_id=23,
)

mag_bridge_spinner = MagBridgeSpinner(spinner_id=34)

# spinner targets
spinner_target1 = PointsSwitch(points_value=50, sound="spinner_points")
spinner_target2 = PointsSwitch(points_value=50, sound="spinner_points")
spinner_target3 = PointsSwitch(points_value=50, sound="spinner_points")
spinner_target4 = PointsSwitch(points_value=50, sound="spinner_points")
spinner_target5 = PointsSwitch(points_value=50, sound="spinner_points")
spinner_target6 = PointsSwitch(points_value=50, sound="spinner_points")
spinner_target7 = PointsSwitch(points_value=50, sound="spinner_points")
spinner_target8 = PointsSwitch(points_value=50, sound="spinner_points")


def init_mag_bridge(game):
    mag_bridge_switch_group.register_message_handlers(game)

    game.register_message_handler(21, mag_bridge.handle_sensor_message)
    game.register_message_handler(23, mag_bridge.handle_mag_bridge_message)
    game.register_message_handler(35, mag_bridge_spinner.handle_spinner_stop)

    game.register_state_handler(mag_bridge.handle_state)
    game.register_state_handler(mag_bridge.handle_plinko_complete)
    game.register_state_handler(mag_bridge_spinner.handle_magbridge_complete)

    game.register_cleanup_handler(mag_bridge.handle_cleanup)
    game.register_cleanup_handler(mag_bridge_spinner.handle_cleanup)

    game.register_message_handler(36, spinner_target1.handle_message)
    game.register_message_handler(37, spinner_target2.handle_message)
    game.register_message_handler(38, spinner_target3.handle_message)
    game.register_message_handler(39, spinner_target4.handle_message)
    game.register_message_handler(40, spinner_target4.handle_message)
    game.register_message_handler(41, spinner_target4.handle_message)
    game.register_message_handler(42, spinner_target4.handle_message)
    game.register_message_handler(43, spinner_target4.handle_message)
