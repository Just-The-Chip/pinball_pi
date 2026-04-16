from comm.constants import COMM_SOLENOIDS
from components.simple_trigger import SimpleTrigger
from components.util import HandlerResponse
from comm.util import build_component_message

launcher = SimpleTrigger(target_id=32)


def force_end(msg, gameState):
    gameState.balls_remaining = 0
    gameState.disable_ball_save()

    return HandlerResponse()


def ball_return(msg, gameState):
    gameState.reduce_balls_in_play()
    # print(f"Balls in play: {gameState.balls_in_play}")
    return HandlerResponse()


def set_game_active(gameState):
    return HandlerResponse(messages=[(COMM_SOLENOIDS, build_component_message(255, True))])


def set_game_inactive(gameState):
    return HandlerResponse(messages=[(COMM_SOLENOIDS, build_component_message(255, False))])


def init_startup(game):
    game.register_startup_handler(set_game_active)
    game.register_cleanup_handler(set_game_inactive)
    game.register_message_handler(2, force_end)
    game.register_message_handler(15, ball_return)
    game.register_launcher_callback(launcher.trigger_component)
