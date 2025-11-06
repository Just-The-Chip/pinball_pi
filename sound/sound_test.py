from pathlib import Path
import os
import sys
import time
from sound import Sound, PLAY_ONCE, PLAY_RANDOM

# add search path so python can find my libraries
curpath = os.path.abspath(os.path.join(__file__, os.pardir))
if (curpath not in sys.path):
    sys.path.append(curpath)

#p = Path('C:\\Users\\sasoc\\Desktop\\Nerd Night\\Pinball sounds\\sorted_sounds\\component sounds\\slider sound.wav')
p = Path('/home/pi/pinball_sounds/sorted_sounds/component sounds')
s = Sound(p, PLAY_ONCE)
s.play()
time.sleep(0.5)
s.stop()
time.sleep(2)
s.play()
time.sleep(1.5)