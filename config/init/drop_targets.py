from components.drop_target import DropTargetGroup

test_group = DropTargetGroup(group_id="test_group", target_ids=(12, 13, 14))


def init_drop_targets(game):
    test_group.register_message_handlers(game)

    # register some state handler to manage teeter totter owr whatevs

    game.register_state_handler(test_group.reset_if_all_triggered)
