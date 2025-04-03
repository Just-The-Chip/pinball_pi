from components.simple_trigger import SimpleTrigger
from components.force_end import ForceEnd

launcher = SimpleTrigger(target_id=32)
startButton = ForceEnd()


def init_startup(game):
    game.register_message_handler(2, startButton.handle_message)
    game.register_startup_handler(launcher.trigger_component)
