class BaseComponent:
    def __init__(self, **kwargs) -> None:
        pass

    def handle_message(self, msg, gameState):
        # decode recieved message
        # update game state
        # queue message to send (optional)
        pass

    def handle_state(self, gameState):
        # check game state for certain conditions
        # queue message(s) to send
        pass
