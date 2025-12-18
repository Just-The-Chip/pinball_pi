from components.drop_target import DropTargetGroup
from components.multiball import Multiball
from config.init.startup import launcher  # I don't love this. May want to refactor somehow.

multiball_drop_targets = DropTargetGroup(
    state_group="multiball_drop_targets",
    target_points=100,
    target_settings=(
        {"component_id": 12, "light_group_id": None},
        {"component_id": 13, "light_group_id": None},
        {"component_id": 14, "light_group_id": None}
    ),
)

multiball = Multiball(
    latch_id=33,
    spool_id=24,
    entry_rollover_id=25,
    drop_target_group=multiball_drop_targets,
    launcher=launcher,
    min_balls=1,
    max_balls=4,
    sound="bikes"
)


def init_multiball(game):
    multiball_drop_targets.register_message_handlers(game)
    game.register_startup_handler(multiball_drop_targets.reset_state_group)

    multiball.register_handlers(game)


def init_drop_targets(game):
    multiball_drop_targets.register_message_handlers(game)

    game.register_startup_handler(multiball_drop_targets.reset_state_group)

    # This functionality may change as we add in multiball
    game.register_state_handler(multiball_drop_targets.reset_if_all_triggered)
