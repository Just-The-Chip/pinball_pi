from components.util import HandlerResponse

def round_end_animation(gameState):
    balls = gameState.balls_remaining + 1
    return HandlerResponse(animation_interrupt={"animation": f"heartloss{balls}", "text": " ", "duration": 3500})
    #return HandlerResponse(animation_interrupt={"animation": "storm", "text": "Test animation", "duration": 5000})

def init_game_end(game):
    game.register_round_end_handler(round_end_animation)