from components.util import HandlerResponse


class BaseComponent:
    def __init__(self, **kwargs) -> None:
        pass

    def handle_message(self, msg, gameState):
        # decode recieved message
        # update game state
        # queue message to send (optional)
        return HandlerResponse()

    def handle_state(self, gameState):
        # check game state for certain conditions
        # queue message(s) to send
        return HandlerResponse()
