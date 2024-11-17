import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from utils import ImageUtils
from constants import GifConstants, MatrixConstants

from PIL import Image
from LEDModes.LEDmode import LEDmode

StartupANI = Image.open(GifConstants.STARTUP)
IdleANI = Image.open(GifConstants.IDLE)

try:
    Startup_num_frames = StartupANI.n_frames
except Exception:
    sys.exit("provided image is not a gif")

try:
    Idle_num_frames = IdleANI.n_frames
except Exception:
    sys.exit("provided image is not a gif")

has_ran_startup = False

class IdleMode(LEDmode):
    
    def __init__(self, matrix):
        self.matrix = matrix

        startupAnimation = Image.open(GifConstants.STARTUP)
        idleAnimation = Image.open(GifConstants.IDLE)

        self.startupCanvases = ImageUtils.compileGif(startupAnimation, matrix)
        self.idleCanvases = ImageUtils.compileGif(idleAnimation, matrix)

        startupAnimation.close()
        idleAnimation.close()


    def startup(self):
        if has_ran_startup:
            self.currentCanvases = self.idleCanvases
            self.currentNumFrames = Idle_num_frames
        else:
            self.currentCanvases = self.startupCanvases
            self.currentNumFrames = Startup_num_frames

        self.cur_frame = 0
        self.start_time = time.time()

        self.matrix.SwapOnVSync(self.currentCanvases[0][0])


    def periodic(self):
        global has_ran_startup
        # display each frame one after the other
        if ((time.time()) - self.start_time) > (self.currentCanvases[1][self.cur_frame] / 1000):
            self.start_time = time.time() # reset timer

            # if the startup animation has finished, switch to the idle animation
            if (self.currentCanvases == self.startupCanvases) and (self.cur_frame == len(self.startupCanvases[0])-1):
                self.cur_frame = 0
                self.currentCanvases = self.idleCanvases
                self.currentNumFrames = Idle_num_frames
                has_ran_startup = True
            else:
                self.cur_frame = (self.cur_frame + 1) % self.currentNumFrames # increment frame counter
            
            self.matrix.SwapOnVSync(self.currentCanvases[0][self.cur_frame]) # go to next frame

        return False
            

    def onEnd(self):
        pass