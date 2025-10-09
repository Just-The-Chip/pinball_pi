from comm.constants import COMM_SOLENOIDS
from comm.util import build_component_message
from components.util import HandlerResponse


class SimpleTrigger:
    def __init__(self, **kwargs) -> None:
        self.target_id: int = kwargs.pop("target_id")
        self.comm_name: str = kwargs.pop("comm_name", COMM_SOLENOIDS)

    def trigger_component(self, _gameState):
        return HandlerResponse(messages=[(self.comm_name, build_component_message(self.target_id))])

    def untrigger_component(self, _gameState):
        return HandlerResponse(messages=[(self.comm_name, build_component_message(self.target_id, 0))])
