from game.state import State
from game.screen import Screen
from comm.comm_handler import CommHandler
from time import time


class Game:

    # message handlers are responsible for interpreting comm messages and changing state and are
    #   called at the beginning of the loop if a message is recieved with a handler's assigned ID.
    #   they return a list of 0 to many (comm_name, message) tuples to add to the comm write queue
    #   Examples:
    #   - add points
    #   - decrease balls remaining
    #   - toggle a drop target flag
    #   - activate a pop bumper light

    # state handlers check the overall state and makes additional changes to the state accordingly
    #   as well return a list of 0 to many (comm_name, message) tuples to add to the comm write queue
    #   if certain conditions in the state are met. all state handlers are called near the end of the loop.
    #   Examples:
    #   - increase a multiplier
    #   - enable a 2nd tier flipper
    #   - release multiball
    #   - reset drop targets

    # Startup handlers will return a list of any messages that need to be sent before the game starts
    #   (e.g. ball launch) They may also modify the state if necessary but I don't see any use for that yet.

    # Cleanup handlers will return a list of messages that need to be sent after the game ends.
    #   They may also do final modications to the state which could affect final score

    def __init__(self, comm_handler, screen) -> None:
        # just start a new game for now but later we will wait for a start signal
        self.comm_handler = comm_handler
        self.screen = screen

        self.in_progress = False
        self.launcher_callback = None
        self.message_handlers = {}

        self.startup_handlers = []
        self.round_start_handlers = []
        self.state_handlers = []
        self.round_end_handlers = []
        self.cleanup_handlers = []

        self.round_start_time = 0
        self.ball_save_start_time = 0

        self.log_messages = False
        self.round_end_pause_length = 7000
        self.ball_save_pause_time = 3500

    def register_launcher_callback(self, callback):
        self.launcher_callback = callback

    def register_message_handler(self, id, handler):
        if id not in self.message_handlers:
            self.message_handlers[id] = []

        self.message_handlers[id].append(handler)

    def register_state_handler(self, handler):
        self.state_handlers.append(handler)
        self.printMsg(f"state handlers: {str(len(self.state_handlers))}")

    def register_startup_handler(self, handler):
        self.startup_handlers.append(handler)
        self.printMsg(f"startup handlers: {str(len(self.startup_handlers))}")

    def register_round_end_handler(self, handler):
        self.round_end_handlers.append(handler)
        self.printMsg(f"round end handlers: {str(len(self.round_end_handlers))}")

    def register_cleanup_handler(self, handler):
        self.cleanup_handlers.append(handler)
        self.printMsg(f"cleanup handlers: {str(len(self.cleanup_handlers))}")

    def execute_launcher(self):
        self.execute_handlers([self.launcher_callback])

    def start(self):
        # send start signal to comms to enable inputs
        # disable start handler/enable message and state handlers?
        self.state = State()
        self.in_progress = True
        self.round_start_time = time() * 1000
        self.ball_save_start_time = 0

        self.execute_handlers(self.startup_handlers)

    def check_start_round(self):
        if self.round_start_time == 0 or (time() * 1000) < self.round_start_time:
            return

        self.printMsg("ROUND START --------------------------------")
        self.screen.set_mode(1)
        self.round_start_time = 0
        self.state.enable_ball_save(15000)  # 15 second grace period
        self.state.add_balls_in_play()
        self.execute_launcher()

    def check_ball_save(self):
        if self.ball_save_start_time == 0 or (time() * 1000) < self.ball_save_start_time:
            return

        self.ball_save_start_time = 0
        self.state.add_balls_in_play()
        self.state.disable_ball_save()
        self.screen.set_mode(1)
        self.execute_launcher()
        self.printMsg("blarp.................................................")

    def check_end_round(self):
        if self.state.balls_in_play > 0 or self.round_start_time > 0 or self.ball_save_start_time > 0:
            return

        now = time() * 1000
        if self.state.ball_save_time >= now:
            self.printMsg("BALL SAVED!!!!!!!!!!!!!!")
            self.ball_save_start_time = now + self.ball_save_pause_time
            self.screen.set_mode(0)
            self.screen.set_display_text("Ball Saved!")
        else:
            self.printMsg("ROUND END ------------------------------")
            self.execute_handlers(self.round_end_handlers)
            self.state.reduce_balls_remaining()
            self.round_start_time = now + self.round_end_pause_length
            self.screen.set_mode(0)
            self.screen.set_display_text(f"BALL OUT!! Lives: {self.state.balls_remaining}")

    def loop(self):
        while self.in_progress:
            self.check_start_round()

            self.handle_incoming_messages()
            self.execute_handlers(self.state_handlers)

            self.check_ball_save()
            self.check_end_round()

            self.comm_handler.write_all_queued()
            self.update_screen()
            self.state.commit_changes()

            if self.state.balls_remaining == 0:
                self.in_progress = False

    def end(self):
        # save high score
        # send end signal to comms to disable inputs, do light patterns, etc.
        # enable start handler/disable message and state handlers?
        self.in_progress = False
        self.execute_handlers(self.cleanup_handlers)
        self.comm_handler.write_all_queued()

    # 00000000  0000 0000
    # ---id---  ---msg---
    def handle_incoming_messages(self):
        messages = self.comm_handler.read_all()
        result_queue = []  # list of tuple results consisting of comm name and message

        # self.printMsg(f"message count: {len(messages)}")
        for id_message in messages:
            int_message = int.from_bytes(id_message, byteorder="big")
            id = (int_message >> 8)
            message = int_message & 255

            self.printMsg(f"MESSAGE ID: {str(id)}")

            handlers = self.message_handlers.get(id, [])
            for handler in handlers:
                result_queue.extend(
                    handler(message, self.state))

            if len(handlers) == 0:
                idString = str(id)
                self.printMsg(f"component id not found: {idString}")

        for comm_name, result_message in result_queue:
            self.comm_handler.queue_message(comm_name, result_message)

    def execute_handlers(self, handlers):
        result_queue = []  # list of tuple results consisting of comm name and message

        for handler in handlers:
            result_queue.extend(handler(self.state))

        if (len(result_queue) > 0):
            self.printMsg(f"RESULT QUEUE: {len(result_queue)}-----------------------")

        for comm_name, result_message in result_queue:
            self.comm_handler.queue_message(comm_name, result_message)

    def update_screen(self):
        self.screen.set_display_score(self.state.score)
        self.screen.set_multiplier(self.state.stacked_multiplier())
        self.screen.set_balls_remaining(self.state.balls_remaining)
        self.screen.update()

    def printMsg(self, message, force=False):
        if self.log_messages or force:
            print(message)
