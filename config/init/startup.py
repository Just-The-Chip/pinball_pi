from components.simple_trigger import SimpleTrigger

launcher = SimpleTrigger(target_id=32)


def force_end(msg, gameState):
    gameState.balls_remaining = 0
    gameState.disable_ball_save()

    return []


def ball_return(msg, gameState):
    gameState.reduce_balls_in_play()
    return []


def init_startup(game):
    game.register_message_handler(2, force_end)
    game.register_message_handler(15, ball_return)
    game.register_launcher_callback(launcher.trigger_component)
