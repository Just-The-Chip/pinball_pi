class DropTarget:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.pop("id")

    def handle_message(self, message, gameState):
        pass

class DropTargetGroup:
    def __init__(self) -> None:
        pass