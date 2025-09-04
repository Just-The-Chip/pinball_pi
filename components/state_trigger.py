from comm.constants import COMM_SERVOS
from comm.util import build_component_message
from components.simple_trigger import SimpleTrigger


class StateTrigger(SimpleTrigger):
    def __init__(self, **kwargs) -> None:
        self.state_key = kwargs.pop("state_key")
        super().__init__(**kwargs)

    def handle_state(self, gameState):
        diff = gameState.get_state_change(self.state_key, False)

        if diff["to"] == True and diff["from"] == False:
            return self.trigger_component(gameState)
        elif diff["to"] == False and diff["from"] == True:
            return self.untrigger_component(gameState)

        return []
