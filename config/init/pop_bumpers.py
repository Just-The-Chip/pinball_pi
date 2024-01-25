from components.points_switch import PointsSwitch

# top bumper
pop_bumper1 = PointsSwitch(points_value=50)

# side bumpers
pop_bumper2 = PointsSwitch(points_value=5)
pop_bumper3 = PointsSwitch(points_value=5)


def init_pop_bumpers(game):
    game.register_message_handler(0, pop_bumper1.handle_message)
    game.register_message_handler(1, pop_bumper2.handle_message)
    game.register_message_handler(2, pop_bumper3.handle_message)
