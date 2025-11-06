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
player.play("points_button")
time.sleep(3)