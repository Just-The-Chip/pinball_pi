from components.simple_state_indicator import SimpleStateIndicator
from components.points_switch import PointsSwitch

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
    game.register_message_handler(45, left_drain_rollover.handle_message)
    game.register_message_handler(46, right_drain_rollover.handle_message)
