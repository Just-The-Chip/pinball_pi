from comm.constants import COMM_SOLENOIDS
from comm.util import build_component_message
from data.constants import IS_PLINKO_ACTIVE


class Plinko:
    def __init__(self, **kwargs) -> None:
        self.lift_id = kwargs.pop("lift_id")
        self.switch_group = kwargs.pop("switch_group")

    def register_message_handlers(self, game):
        for target_id in self.switch_group.target_ids:
            game.register_message_handler(target_id, self.handle_plinko_stop)

    def handle_plinko_start(self, gameState):
        is_plinko = gameState.get_state_change(IS_PLINKO_ACTIVE, False)

        if is_plinko["from"] == False and is_plinko["to"] == True:
            return self.start_lift()

        return []

    def update_multiplier(self, gameState):
        gameState.set_multiplier("plinko", self.switch_group.triggered_count(gameState))

        return []

    def start_lift(self):
        return [(COMM_SOLENOIDS, build_component_message(self.lift_id))]

    def handle_plinko_stop(self, message, gameState):
        gameState.set_state(IS_PLINKO_ACTIVE, False)
        return []
