from components.mag_bridge import MagBridge

mag_bridge = MagBridge(
    state_group="mag_bridge_switches",
    target_ids=(17, 18, 19, 20),
    rejector_id=22,
    mag_bridge_id=23,
    target_points=100
)


def init_mag_bridge(game):
    mag_bridge.register_message_handlers(game)

    game.register_message_handler(21, mag_bridge.handle_message)
