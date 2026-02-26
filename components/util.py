from typing_extensions import Self

Message = tuple[str, bytes]

PLAY: int = 0
STOP: int = 1

class HandlerResponse:
    def __init__(self, **kwargs):
        self.messages: list[Message] = kwargs.pop("messages", [])
        
        sounds = kwargs.pop("sounds", []) # can also be a single str
        if isinstance(sounds, str):             # kwarg is a string
            self.sounds = [(sounds, PLAY)]
        elif isinstance(sounds, tuple):    # kwarg is a tuple with sound alias and play option
            self.sounds = [sounds]
        elif sounds == None:                    # kwarg is None
            self.sounds = []
        else:
            self.sounds = sounds                #kwarg is probably an empty array

    def extend_messages(self, messages: list[Message]):
        self.messages.extend(messages)

    def append_message(self, message: Message):
        self.messages.append(message)

    #NOT USED
    def extend_sounds(self, sounds: list[str]):
        self.sounds.extend(sounds)
    #NOT USED
    def append_sound(self, sound: str, mode: int = PLAY):
        self.sounds.append((sound, mode))

    def extend(self, response: Self):
        self.messages.extend(response.messages)
        self.sounds.extend(response.sounds)
