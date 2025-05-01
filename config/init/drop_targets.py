from components.drop_target import DropTargetGroup

multiball_drop_targets = DropTargetGroup(
    state_group="multiball_drop_targets",
    target_settings=(
        {"component_id": 12, "light_group_id": None},
        {"component_id": 13, "light_group_id": None},
        {"component_id": 14, "light_group_id": None}
    ),
)


def init_drop_targets(game):
    multiball_drop_targets.register_message_handlers(game)

    game.register_startup_handler(multiball_drop_targets.reset_state_group)

    # This functionality may change as we add in multiball
    game.register_state_handler(multiball_drop_targets.reset_if_all_triggered)
