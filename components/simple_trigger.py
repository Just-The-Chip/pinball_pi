from comm.constants import COMM_SOLENOIDS
from comm.util import build_component_message


class SimpleTrigger:
    def __init__(self, **kwargs) -> None:
        self.target_id = kwargs.pop("target_id")
        self.comm_name = kwargs.pop("comm_name", COMM_SOLENOIDS)

    def trigger_component(self, gameState):
        return [(self.comm_name, build_component_message(self.target_id))]
