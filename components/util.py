from typing_extensions import Self

Message = tuple[str, bytes]

PLAY: int = 0
STOP: int = 1


class HandlerResponse:
    def __init__(self, **kwargs):
        self.messages: list[Message] = kwargs.pop("messages", [])
        self.animation_interrupt: dict = kwargs.pop("animation_interrupt", None)
        
        sounds = kwargs.pop("sounds", [])
        self.sounds = self._format_sounds(sounds)

    def extend_messages(self, messages: list[Message]):
        self.messages.extend(messages)

    def append_message(self, message: Message):
        self.messages.append(message)

    # NOT USED
    def extend_sounds(self, sounds: list[str]):
        self.sounds.extend(sounds)

    def append_sound(self, sound: str, mode: int = PLAY):
        self.sounds.append((sound, mode))

    def extend(self, response: Self):
        self.messages.extend(response.messages)
        self.sounds.extend(response.sounds)

        if response.animation_interrupt is not None:
            self.animation_interrupt = response.animation_interrupt
    def _format_sounds(self, sounds):   #formats a given sound type to our prefered type: array[tuple(str, int)]
        if isinstance(sounds, str):             # kwarg is a string
            sound_out = [(sounds, PLAY)]
        elif isinstance(sounds, tuple):    # kwarg is a tuple with sound alias and play option
            sound_out = [sounds]
        elif sounds == None:                    # kwarg is None
            sound_out = []
        else:
            sound_out = sounds                #kwarg is probably an empty array
        return sound_out
