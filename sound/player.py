from sound import Sound, PLAY_ONCE, PLAY_RANDOM
from pathlib import Path

class Player:

    def __init__(self):
        self.sound_dir = Path("/home/pi/pinball_sounds/sorted_sounds")
        self.sound_lib = {} # dictionary of every sound or sound group
        self.loadsounds()

    # load all the sounds into some object so they can be called by name
    def loadsounds(self):
        self.sound_lib["points_button"] = Sound(self.sound_dir / 'component sounds/points buttons', PLAY_RANDOM)
        self.sound_lib["pop_bumper"] = Sound(self.sound_dir / 'component sounds/Poppers', PLAY_RANDOM)

    # game calls this to play a sound
    def play(self, alias: str):
        print("PLAY PLAY PLAY")
        self.sound_lib[alias].play()
    
    # game call this to stop a sound that is playing
    def stop(self, alias: str):
        self.sound_lib[alias].stop()