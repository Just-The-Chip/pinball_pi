from components.plinko import Plinko
from components.state_switch_group import StateSwitchGroup

plinko_switch_group = StateSwitchGroup(
    state_group="plinko_switches",
    target_settings=(
        {"component_id": 27, "light_group_id": None},
        {"component_id": 28, "light_group_id": None},
        {"component_id": 29, "light_group_id": None},
        {"component_id": 30, "light_group_id": None}
    ),
    target_points=2000
)

plinko = Plinko(
    lift_id=26,
    switch_group=plinko_switch_group
)


def init_plinko(game):
    plinko_switch_group.register_message_handlers(game)
    plinko.register_message_handlers(game)

    game.register_state_handler(plinko.handle_plinko_start)
