from pathlib import Path
import os
import sys
import time
from player import Player

# add search path so python can find my libraries
#curpath = os.path.abspath(os.path.join(__file__, os.pardir))
#if (curpath not in sys.path):
#    sys.path.append(curpath)

#p = Path('C:\\Users\\sasoc\\Desktop\\Nerd Night\\Pinball sounds\\sorted_sounds\\component sounds\\slider sound.wav')
player = Player()

all_sounds = ["points_button","pop_bumper","spinner_points","mario_tube","bikes","game_start","game_end","round_end","circus","slingshot","rear_popper","finale_reject","ball_save_solenoid","finale_unlock","multiball_deposit","unlock_left_launcher","double_kill","headshot","triple_kill","goat","ball_drain_save","slide1","slide2","slide3","slide4","slide5","slide7"]

for sound in all_sounds:
    player.play(sound)
    time.sleep(8)