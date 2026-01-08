# class representing a single sound, or a group of sounds
from just_playback import Playback
from pathlib import Path
from random import random
#from typing import List

#PLAYBACK MODES:
PLAY_ONCE = 0 # play one sound from the set, in order by sound file name
PLAY_RANDOM = 1 # plays random sound from the set
LOOP = 2 # loops the sound continuously until the stop method is called

class Sound:
    def __init__(self, path: Path, playback_mode: int): # path: path to a sound file, or folder of sound files
        self.playback_mode = playback_mode
        self.sounds = [] # list of sound objects
        self.sound_idx = 0 # keeps track of what sound should play next
        self.last_sound = 0 # keeps track of the last sound that played
        self.load_sounds(path)
            
    # loads the sound or sounds from path.  If path is a folder, it loads everything in the folder.
    def load_sounds(self, path: Path):
        if path.is_dir(): # there are multiple sound files
            for file_name in path.iterdir(): # if item is not a directory, load it as a sound object
                if not file_name.is_dir():
                    self.sounds.append(Playback(str(file_name)))
        else: # there is only one sound file
            self.sounds.append(Playback(str(path)))

    def play(self):
        if self.playback_mode == LOOP:
            self.sounds[self.sound_idx].loop_at_end(True)
        self.sounds[self.sound_idx].play()
        self.last_sound = self.sound_idx
        
        if self.playback_mode == PLAY_ONCE: # Increment sound index
            self.sound_idx += 1
            if self.sound_idx >= len(self.sounds):
                self.sound_idx = 0
        if self.playback_mode == PLAY_RANDOM: # Set sound index to random number
            self.sound_idx = int(random() * (len(self.sounds)-1))

    def stop(self):
        self.sounds[self.last_sound].stop()