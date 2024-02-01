class PointsSwitch:
    points_value = 5

    def __init__(self, **kwargs) -> None:
        self.base_points = kwargs.pop("points_value", 5)

    def handle_message(self, msg, gameState):
        gameState.add_points(self.base_points)
        return []  # must return empty results
