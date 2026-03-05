from PIL import Image, ImageEnhance
from typing import TypedDict

IMAGE_DIR = "/home/pi/pinball_images/"
FRAME_LIMIT = 1000


class FrameData(TypedDict):
    image: Image.Image
    duration: float
    text_color: list[int, int, int] = (255, 255, 255)


class Animation:
    def __init__(self, name: str, path: str, brightness: float, text_color=(255, 255, 255)):
        self.name = name
        self.path = path
        self.brightness = brightness
        self.text_color = text_color

        self.frames: list[FrameData] = []

    def load_frames(self):
        self.frames = []

        # todo: sanitize path
        gif = Image.open(f"{IMAGE_DIR}{self.path}")
        frame_count = min(getattr(gif, "n_frames", 1), FRAME_LIMIT)
        brightness = self.brightness if self.brightness <= 1.0 and self.brightness >= 0.0 else 1.0

        for i in range(frame_count):
            # idk if we need try catch, verify later.
            try:
                gif.seek(i)
            except (EOFError, IndexError, OSError):
                break

            duration = gif.info.get("duration", 100)

            frame = gif.copy().convert("RGB")

            enhancer = ImageEnhance.Brightness(frame)
            enhanced_frame = enhancer.enhance(brightness)

            self.frames.append(FrameData(
                image=enhanced_frame,
                duration=duration
            ))

    def get_frame(self, index: int) -> FrameData:
        return self.frames[index]

    def frame_count(self) -> int:
        return len(self.frames)

    def total_duration(self) -> float:
        return sum(frame["duration"] for frame in self.frames)
