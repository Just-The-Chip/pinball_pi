from components.mag_bridge import MagBridge

mag_bridge = MagBridge(
    state_group="mag_bridge_switches",
    target_settings=(
        {"component_id": 17, "light_group_id": 6},
        {"component_id": 18, "light_group_id": 7},
        {"component_id": 19, "light_group_id": 8},
        {"component_id": 20, "light_group_id": 9}
    ),
    ball_catch_light_group=11,
    rejector_id=22,
    mag_bridge_id=23,
    target_points=100
)


def init_mag_bridge(game):
    mag_bridge.register_message_handlers(game)

    game.register_message_handler(21, mag_bridge.handle_sensor_message)
    game.register_message_handler(23, mag_bridge.handle_mag_bridge_message)
    game.register_state_handler(mag_bridge.handle_state)
