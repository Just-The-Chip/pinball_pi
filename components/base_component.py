from components.util import HandlerResponse


class BaseComponent:
    def __init__(self, **kwargs) -> None:
        self.sound: str = kwargs.pop("sound") # string representing the sound or sound group of the component

    def handle_message(self, msg, gameState):
        # decode recieved message
        # update game state
        # queue message to send (optional)
        return HandlerResponse()

    def handle_state(self, gameState):
        # check game state for certain conditions
        # queue message(s) to send
        return HandlerResponse()
