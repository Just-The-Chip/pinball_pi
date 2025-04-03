from components.points_switch import PointsSwitch

# slingshots (maybe I'll move this later)
leftSling = PointsSwitch(points_value=50, light_group_id=4)
rightSling = PointsSwitch(points_value=50, light_group_id=5)

# top bumper
pop_bumper1 = PointsSwitch(points_value=500, light_group_id=1, pattern_id=2)

# side bumpers
pop_bumper2 = PointsSwitch(points_value=150, light_group_id=2)
pop_bumper3 = PointsSwitch(points_value=150, light_group_id=3)

# left static targets
left_target1 = PointsSwitch(points_value=100, light_group_id=19, pattern_id=3, pattern_option=2)
left_target2 = PointsSwitch(points_value=100, light_group_id=18, pattern_id=3, pattern_option=2)
left_target3 = PointsSwitch(points_value=100, light_group_id=17, pattern_id=3, pattern_option=2)
left_target4 = PointsSwitch(points_value=100, light_group_id=16, pattern_id=3, pattern_option=2)


def init_pop_bumpers(game):
    game.register_message_handler(0, leftSling.handle_message)
    game.register_message_handler(1, rightSling.handle_message)

    # ball return and start button have IDs 2 and 3

    game.register_message_handler(4, pop_bumper1.handle_message)
    game.register_message_handler(5, pop_bumper2.handle_message)
    game.register_message_handler(6, pop_bumper3.handle_message)

    game.register_message_handler(7, left_target1.handle_message)
    game.register_message_handler(8, left_target2.handle_message)
    game.register_message_handler(9, left_target3.handle_message)
    # 10 is ascii for \n so we skip
    game.register_message_handler(11, left_target4.handle_message)
