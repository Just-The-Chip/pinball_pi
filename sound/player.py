from sound import Sound, PLAY_ONCE, PLAY_RANDOM, LOOP
from pathlib import Path

class Player:

    def __init__(self):
        self.sound_dir = Path("/home/pi/pinball_sounds/sorted_sounds")
        self.sound_lib = {} # dictionary of every sound or sound group
        self.loadsounds()
        self.muted = False

    # load all the sounds into some object so they can be called by name
    def loadsounds(self):
        self.sound_lib["points_button"] = Sound(self.sound_dir / 'component sounds/points buttons', PLAY_RANDOM)
        self.sound_lib["pop_bumper"] = Sound(self.sound_dir / 'component sounds/Poppers', PLAY_RANDOM)
        self.sound_lib["spinner_points"] = Sound(self.sound_dir / 'component sounds/Spinner buttons', PLAY_RANDOM)
        self.sound_lib["mario_tube"] = Sound(self.sound_dir / 'component sounds/mario tube', PLAY_RANDOM)
        self.sound_lib["bikes"] = Sound(self.sound_dir / 'component sounds/multi-ball drop (bikes).mp3', PLAY_ONCE)
        self.sound_lib["game_start"] = Sound(self.sound_dir / 'game start', PLAY_RANDOM)
        self.sound_lib["game_end"] = Sound(self.sound_dir / 'game end', PLAY_RANDOM)
        self.sound_lib["round_end"] = Sound(self.sound_dir / 'round end', PLAY_RANDOM)
        self.sound_lib["circus"] = Sound(self.sound_dir / 'songs/circus-music-388517.mp3', LOOP)
        self.sound_lib["slingshot"] = Sound(self.sound_dir / 'component sounds/slingshot', PLAY_RANDOM)
        self.sound_lib["rear_popper"] = Sound(self.sound_dir / 'component sounds/rear_popper.mp3', PLAY_ONCE)
        self.sound_lib["finale_reject"] = Sound(self.sound_dir / 'component sounds/finale_rejected.mp3', PLAY_ONCE)
        self.sound_lib["ball_save_solenoid"] = Sound(self.sound_dir / 'component sounds/ball-save-spring.mp3', PLAY_ONCE)
        self.sound_lib["finale_unlock"] = Sound(self.sound_dir / 'component sounds/finale-unlock.mp3', PLAY_ONCE)
        self.sound_lib["multiball_deposit"] = Sound(self.sound_dir / 'component sounds/multi-ball-deposit.mp3', PLAY_ONCE)
        self.sound_lib["unlock_left_launcher"] = Sound(self.sound_dir / 'component sounds/left-launcher-unlock.mp3', PLAY_ONCE)
        self.sound_lib["double_kill"] = Sound(self.sound_dir / 'component sounds/unreal sounds/01_double kill.wav', PLAY_ONCE)
        self.sound_lib["headshot"] = Sound(self.sound_dir / 'component sounds/unreal sounds/00_headshot.wav', PLAY_ONCE)
        self.sound_lib["triple_kill"] = Sound(self.sound_dir / 'component sounds/unreal sounds/02_triple kill.wav', PLAY_ONCE)
        self.sound_lib["goat"] = Sound(self.sound_dir / 'goats', PLAY_RANDOM)
        self.sound_lib["ball_drain_save"] = Sound(self.sound_dir / 'Notifications/ball_drain_save.mp3', PLAY_ONCE)
        self.sound_lib["slide1"] = Sound(self.sound_dir / 'component sounds/slider/2.wav', PLAY_ONCE)
        self.sound_lib["slide2"] = Sound(self.sound_dir / 'component sounds/slider/3.wav', PLAY_ONCE)
        self.sound_lib["slide3"] = Sound(self.sound_dir / 'component sounds/slider/4.wav', PLAY_ONCE)
        self.sound_lib["slide4"] = Sound(self.sound_dir / 'component sounds/slider/5.wav', PLAY_ONCE)
        self.sound_lib["slide5"] = Sound(self.sound_dir / 'component sounds/slider/6.wav', PLAY_ONCE)
        self.sound_lib["slide7"] = Sound(self.sound_dir / 'component sounds/slider/7.wav', PLAY_ONCE)

    # game calls this to play a sound
    def play(self, alias: str):
        if (not self.muted) or alias == "game_end": # if muted, only play the game_end sound
            if alias in self.sound_lib:
                self.sound_lib[alias].play()
            else:
                print("INVALID SOUND [", alias,"] PLAYED")
        else:
            print("MUTED")
    
    # game call this to stop a sound that is playing
    def stop(self, alias: str):
        self.sound_lib[alias].stop()
    
    # when game is muted, only the game_end sound plays.  This prevents overlapping round-end and multi-ball drop sounds.
    def mute(self):
        self.muted = True
    
    def unmute(self):
        self.muted = False