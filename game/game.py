from game.state import State
from game.screen import Screen
from comm.comm_handler import CommHandler


class Game:

    # message handlers are responsible for interpreting comm messages and changing state and are
    #   called at the beginning of the loop if a message is recieved with a handler's assigned ID.
    #   they return a list of 0 to many (comm_name, message) tuples to add to the comm write queue
    #   Examples:
    #   - add points
    #   - decrease balls remaining
    #   - toggle a drop target flag
    #   - activate a pop bumper light
    message_handlers = {}

    # state handlers check the overall state and makes additional changes to the state accordingly
    #   as well return a list of 0 to many (comm_name, message) tuples to add to the comm write queue
    #   if certain conditions in the state are met. all state handlers are called near the end of the loop.
    #   Examples:
    #   - increase a multiplier
    #   - enable a 2nd tier flipper
    #   - release multiball
    #   - reset drop targets
    state_handlers = []

    in_progress = False

    def __init__(self, comm_handler, font, multiplier_font) -> None:
        # just start a new game for now but later we will wait for a start signal
        self.comm_handler = comm_handler
        self.screen = Screen(font=font, multiplier_font=multiplier_font)
        self.start()

    def register_message_handler(self, id, handler):
        if id not in self.message_handlers:
            self.message_handlers[id] = []

        self.message_handlers[id].append(handler)

    def register_state_handler(self, handler):
        self.state_handlers.append(handler)
        print(f"state handlers: {str(len(self.state_handlers))}")

    def start(self):
        # send start signal to comms to enable inputs
        # disable start handler/enable message and state handlers?
        self.state = State()
        self.in_progress = True

    def loop(self):
        while self.in_progress:
            self.handle_incoming_messages()
            self.handle_state()
            self.comm_handler.write_all_queued()
            self.update_screen()
            self.state.commit_changes()

        self.end()

    def end(self):
        # save high score
        # send end signal to comms to disable inputs, do light patterns, etc.
        # enable start handler/disable message and state handlers?
        self.in_progress = False

    # 00000000  0000 0000
    # ---id---  ---msg---
    def handle_incoming_messages(self):
        messages = self.comm_handler.read_all()
        result_queue = []  # list of tuple results consisting of comm name and message

        # print(f"message count: {len(messages)}")
        for id_message in messages:
            int_message = int.from_bytes(id_message, byteorder="big")
            id = (int_message >> 8)
            message = int_message & 255

            handlers = self.message_handlers.get(id, [])
            for handler in handlers:
                result_queue.extend(
                    handler(message, self.state))

            if len(handlers) == 0:
                print(f"component id not found: {str(id)}")

        for comm_name, result_message in result_queue:
            self.comm_handler.queue_message(comm_name, result_message)

    def handle_state(self):
        result_queue = []  # list of tuple results consisting of comm name and message

        for handler in self.state_handlers:
            result_queue.extend(handler(self.state))

        if (len(result_queue) > 0):
            print(f"RESULT QUEUE: {len(result_queue)}-----------------------")

        for comm_name, result_message in result_queue:
            self.comm_handler.queue_message(comm_name, result_message)

    def update_screen(self):
        self.screen.set_display_score(self.state.score)
        self.screen.set_multiplier(self.state.stacked_multiplier())
        self.screen.update()
