from typing_extensions import Self

Message = tuple[str, bytes]


class HandlerResponse:
    def __init__(self, **kwargs):
        self.messages: list[Message] = kwargs.pop("messages", [])
        self.sounds: list[str] = kwargs.pop("sounds", [])

    def extend_messages(self, messages: list[Message]):
        self.messages.extend(messages)

    def append_message(self, message: Message):
        self.messages.append(message)

    def extend_sounds(self, sounds: list[str]):
        self.sounds.extend(sounds)

    def append_sound(self, sound: str):
        self.sounds.append(sound)

    def extend(self, response: Self):
        self.messages.extend(response.messages)
        self.sounds.extend(response.sounds)
