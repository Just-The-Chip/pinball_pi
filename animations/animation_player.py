
from animations.animation import Animation, FrameData
from rgbmatrix import graphics
from time import perf_counter
import yaml


class AnimationPlayer:
    def __init__(self, **kwargs):
        self.animation_dict: dict[str, Animation] = {}
        self.font = kwargs.get("font")

        self.animation: Animation = None
        self.current_frame_index = 0
        self.current_frame: FrameData = None
        self.current_frame_start_time = 0
        self.animation_start_time = 0
        self.duration = 0
        self.text = None
        self.text_color = (255, 255, 255)
        self.scroll_speed = 1
        self.canvas_width = 64

        self.text_position = 0

    def load_animations(self, config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        for anim_config in config["animations"]:
            name = anim_config["name"]
            path = anim_config["path"]
            brightness = anim_config.get("brightness", 1.0)
            text_color = tuple(anim_config.get("text_color", (255, 255, 255)))

            animation = Animation(name, path, brightness, text_color)
            animation.load_frames()
            self.animation_dict[name] = animation

    def start_animation(self, **kwargs):
        print("ANIMATION SETTONGS: ")
        print(kwargs)
        self.animation = self.animation_dict.get(kwargs.get("animation", None), None)
        self.text = kwargs.get("text", None)
        self.scroll_speed = kwargs.get("scroll_speed", 1)
        self.canvas_width = kwargs.get("canvas_width", 64)

        self.text_position = self.canvas_width
        self.current_frame_index = 0

        default_duration = self.animation.total_duration() if self.animation else 0
        self.duration = kwargs.get("duration", default_duration)

        default_text_color_rgb = self.animation.text_color if self.animation else (255, 255, 255)
        text_color_rgb = kwargs.get("text_color", default_text_color_rgb)
        self.text_color = graphics.Color(*text_color_rgb)

        if self.animation is not None:
            self.current_frame = self.animation.get_frame(self.current_frame_index)
            self.animation_start_time = perf_counter() * 1000
            self.current_frame_start_time = self.animation_start_time

    def clear_animation(self):
        self.animation = None
        self.current_frame_index = 0
        self.current_frame = None
        self.current_frame_start_time = 0
        self.animation_start_time = 0
        self.duration = 0
        self.text = None
        self.text_color = (255, 255, 255)
        self.scroll_speed = 1
        self.canvas_width = 64

        self.text_position = 0

    def update(self, canvas):
        if self.animation is None or not self.text:
            return

        self.draw_frame(canvas)
        self.draw_text(canvas)

    def draw_frame(self, canvas):
        if self.animation is None:
            return

        now = perf_counter() * 1000
        elapsed_time = now - self.current_frame_start_time

        next_frame_index, next_frame = self.animation.get_next_frame(
            self.current_frame_index, elapsed_time)

        if next_frame is not None and next_frame_index != self.current_frame_index:
            self.current_frame_index = next_frame_index
            self.current_frame = next_frame
            self.current_frame_start_time = now

        canvas.SetImage(self.current_frame["image"], 0, 0)

    def draw_text(self, canvas):
        if not self.text:
            return

        length = graphics.DrawText(canvas, self.font,
                                   self.text_position, 15, self.text_color, self.text)

        self.text_position -= self.scroll_speed

        if self.text_position + length < 0:
            self.text_position = self.canvas_width

    def is_done(self) -> bool:
        return self.animation_start_time + self.duration <= perf_counter() * 1000
