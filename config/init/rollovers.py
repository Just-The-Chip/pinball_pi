from components.simple_state_indicator import SimpleStateIndicator
from components.points_switch import PointsSwitch

# flash on pattern
ballSaveIndicator = SimpleStateIndicator(
    light_group_id=23,
    pattern_id=6,
    variant_id=1,
    pattern_option=3,
    indicator_key="ball_save_indicator",
    state_callback=lambda gameState: gameState.is_ball_save_active()
)

left_drain_rollover = PointsSwitch(
    points_value=0,
    light_group_id=21,
    pattern_id=3,
    variant_id=0,
    pattern_option=3,
    should_cycle_variants=False
)
right_drain_rollover = PointsSwitch(
    points_value=0,
    light_group_id=22,
    pattern_id=3,
    variant_id=0,
    pattern_option=3,
    should_cycle_variants=False
)


def init_rollovers(game):
    # TODO: flash side lights on rollover (probably red)
    game.register_state_handler(ballSaveIndicator.handle_state)
    game.register_cleanup_handler(ballSaveIndicator.handle_cleanup)

    game.register_message_handler(45, left_drain_rollover.handle_message)
    game.register_message_handler(46, right_drain_rollover.handle_message)
