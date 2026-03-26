from comm.constants import COMM_SOLENOIDS
from comm.util import build_component_message
from components.util import HandlerResponse


class SimpleTrigger:
    def __init__(self, **kwargs) -> None:
        self.target_id: int = kwargs.pop("target_id")
        self.comm_name: str = kwargs.pop("comm_name", COMM_SOLENOIDS)
        self.trigger_sound: str = kwargs.pop("trigger_sound", "")
        self.untrigger_sound: str = kwargs.pop("untrigger_sound", "")

    def trigger_component(self, _gameState):
        return HandlerResponse(messages=[(self.comm_name, build_component_message(self.target_id))], sounds=self.trigger_sound)

    def untrigger_component(self, _gameState):
        return HandlerResponse(messages=[(self.comm_name, build_component_message(self.target_id, 0))], sounds=self.untrigger_sound)