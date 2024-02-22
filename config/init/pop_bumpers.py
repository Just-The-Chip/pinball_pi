from components.points_switch import PointsSwitch

# slingshots (maybe I'll move this later)
leftSling = PointsSwitch(points_value=5)
rightSling = PointsSwitch(points_value=5)

# top bumper
pop_bumper1 = PointsSwitch(points_value=50)

# side bumpers
pop_bumper2 = PointsSwitch(points_value=10)
pop_bumper3 = PointsSwitch(points_value=10)


def init_pop_bumpers(game):
    game.register_message_handler(0, leftSling.handle_message)
    game.register_message_handler(1, rightSling.handle_message)

    # ball return and launch have IDs 2 and 3 but they don't do any game stuff yet

    game.register_message_handler(4, pop_bumper1.handle_message)
    game.register_message_handler(5, pop_bumper2.handle_message)
    game.register_message_handler(6, pop_bumper3.handle_message)
