import time
import sys

from utils import ImageUtils

from rgbmatrix import RGBMatrix

from PIL import Image
from LEDModes.LEDmode import LEDmode


class GifMode(LEDmode):
    def __init__(self, matrix: RGBMatrix, gifPath: str, endThyself: bool = False):
        self.matrix = matrix
        self.endThyself = endThyself
        animation = Image.open(gifPath)

        try:
            self.num_frames = animation.n_frames
        except Exception:
            sys.exit("provided image is not a gif")

        self.gifCanvases = ImageUtils.compileGif(animation, matrix)
        animation.close()

    def startup(self):
        self.cur_frame = 0
        self.start_time = time.time()

        self.matrix.SwapOnVSync(self.gifCanvases[0][0])

    def periodic(self):
        # display each frame one after the other
        if ((time.time()) - self.start_time) > (self.gifCanvases[1][self.cur_frame] / 1000):
            self.start_time = time.time() # reset timer

            # If the gif has reached its end, end the mode if endThyself is set to True
            if (self.cur_frame >= self.num_frames - 1) and self.endThyself:
                return True
            else:
                self.cur_frame = (self.cur_frame + 1) % self.num_frames

            self.matrix.SwapOnVSync(self.gifCanvases[0][self.cur_frame]) # go to next frame

        return False

    def onEnd(self):
        pass