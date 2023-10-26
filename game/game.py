from state import State
from comm.comm_handler import CommHandler

class Game:

    # message handlers are responsible for interpreting comm messages and changing state and are
    #   called at the beginning of the loop if a message is recieved with a handler's assigned ID.  
    #   they may also queue messages to send to the light comm.
    #   Examples:
    #   - add points
    #   - decrease balls remaining
    #   - toggle a drop target flag
    #   - activate a pop bumper light
    message_handlers = {}

    # state handlers check the overall state and makes additional changes to the state accordingly
    #   as well as queue up messages if certain conditions in the state are met.
    #   all state handlers are called at the end of the loop.
    #   Examples:
    #   - increase a multiplier
    #   - enable a 2nd tier flipper
    #   - release multiball
    #   - reset drop targets
    state_handlers = []

    def __init__(self, comm_handler) -> None:
        # just start a new game for now but later we will wait for a start signal
        self.comm_handler = comm_handler
        self.start()

    def register_message_handler(self, id, handler):
        self.message_handlers[id] = handler

    def register_state_handler(self, handler):
        self.state_handlers.append(handler)

    def start(self):
        # send start signal to comms to enable inputs
        # disable start handler/enable message and state handlers?
        self.state = State()

    def end(self):
        # save high score
        # send end signal to comms to disable inputs, do light patterns, etc.
        # enable start handler/disable message and state handlers?
        pass 