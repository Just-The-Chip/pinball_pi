from components.mag_bridge import MagBridge
from components.state_switch_group import StateSwitchGroup

mag_bridge_switch_group = StateSwitchGroup(
    state_group="mag_bridge_switches",
    target_settings=(
        {"component_id": 17, "light_group_id": 6},
        {"component_id": 18, "light_group_id": 7},
        {"component_id": 19, "light_group_id": 8},
        {"component_id": 20, "light_group_id": 9}
    ),
    target_points=100
)

mag_bridge = MagBridge(
    switch_group=mag_bridge_switch_group,
    ball_catch_light_group=11,
    ball_catch_variant_id=0,
    rejector_id=22,
    mag_bridge_id=23,
)


def init_mag_bridge(game):
    mag_bridge_switch_group.register_message_handlers(game)

    game.register_message_handler(21, mag_bridge.handle_sensor_message)
    game.register_message_handler(23, mag_bridge.handle_mag_bridge_message)
    game.register_state_handler(mag_bridge.handle_state)
    game.register_state_handler(mag_bridge.handle_plinko_complete)
    game.register_cleanup_handler(mag_bridge.handle_cleanup)
