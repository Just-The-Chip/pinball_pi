from comm.constants import COMM_SOLENOIDS, COMM_SERVOS
from comm.util import build_component_message
from time import time


class Multiball:
    def __init__(self, **kwargs) -> None:
        self.spool_id = kwargs.pop("spool_id")
        self.latch_id = kwargs.pop("latch_id")
        self.entry_rollover_id = kwargs.pop("entry_rollover_id")
        self.drop_target_group = kwargs.pop("drop_target_group")
        self.launcher = kwargs.pop("launcher")
        self.min_balls = kwargs.pop("min_balls", 1)
        self.max_balls = kwargs.pop("max_balls", 3)

        self.spool_on_time = 1000
        self.latch_trigger_delay = 500

        self.bank_ready_key = "multiball_bank_ready"
        self.bank_count_key = "multiball_bank_count"
        self.latch_trigger_time_key = "latch_trigger_time"
        self.log_messages = False

    def bank_ready(self, gameState):
        return gameState.get_state(self.bank_ready_key, False)

    def bank_count(self, gameState):
        return gameState.get_state(self.bank_count_key, 0)

    def latch_trigger_time(self, gameState):
        return gameState.get_state(self.latch_trigger_time_key, 0)

    def register_handlers(self, game):
        game.register_message_handler(self.entry_rollover_id, self.handle_ball_entry)
        game.register_state_handler(self.handle_state)
        game.register_state_handler(self.handle_door_latch)
        game.register_cleanup_handler(self.release_multiball)

    def handle_ball_entry(self, msg, gameState):
        # may need special handling for if door is the process of closing
        if not self.bank_ready(gameState):
            return []

        bank_count = self.bank_count(gameState) + 1

        if bank_count > self.max_balls:
            return self.release_multiball(gameState)

        gameState.set_state(self.bank_count_key, bank_count)
        self.printMsg(f"Multiball bank count: {bank_count}")

        return self.launcher.trigger_component(gameState)

    def handle_door_latch(self, gameState):
        trigger_time = self.latch_trigger_time(gameState)

        if (self.bank_ready(gameState) and trigger_time > 0 and trigger_time <= time() * 1000):
            self.printMsg("TRIGGER THE LATCH!!!!")
            gameState.set_state(self.latch_trigger_time_key, 0)
            return [(COMM_SERVOS, build_component_message(self.latch_id, 1))]

        return []

    def handle_state(self, gameState):
        dropTargetsActivated = self.drop_target_group.is_group_fully_triggered(gameState)
        if not dropTargetsActivated or gameState.balls_in_play > 1:
            return []

        result_queue = self.drop_target_group.reset_state_group(gameState)

        if self.bank_count(gameState) >= self.min_balls:
            result_queue.extend(self.release_multiball(gameState))
        elif not self.bank_ready(gameState):
            result_queue.extend(self.close_door(gameState))

        return result_queue

    def release_multiball(self, gameState):
        self.printMsg("RELEASE MULTIBALL")
        bank_count = self.bank_count(gameState)
        gameState.add_balls_in_play(bank_count)
        self.printMsg(f"Balls in play RELEASE: {gameState.balls_in_play}")

        gameState.set_state(self.bank_count_key, 0)
        gameState.set_state(self.bank_ready_key, False)
        return [(COMM_SERVOS, build_component_message(self.latch_id, 0))]

    def close_door(self, gameState):
        self.printMsg("CLOSE THE DOOR!")
        # set some sort of timestamp so that we can latch the door after it's closed
        gameState.set_state(self.bank_ready_key, True)

        latch_time = (time() * 1000) + self.latch_trigger_delay
        gameState.set_state(self.latch_trigger_time_key, latch_time)

        # 10ths of a second
        spool_time = round(self.spool_on_time / 100)
        spool_time = spool_time if spool_time < 10 else spool_time + 1
        return [(COMM_SOLENOIDS, build_component_message(self.spool_id, spool_time))]

    def printMsg(self, message):
        if self.log_messages:
            print(message)
