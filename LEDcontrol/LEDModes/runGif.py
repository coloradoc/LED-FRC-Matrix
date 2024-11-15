import time
import sys

from utils import ImageUtils
from constants import MatrixConstants

from rgbmatrix import RGBMatrix

from PIL import Image
from LEDModes.LEDmode import LEDmode


def compileGif(gif: Image.Image, matrix) -> list:
    """
    Takes a gif and returns a tuple containing a list of canvases that can be 
    displayed one after the other, along with the duration of the gif.
    """

    canvases = []
    
    # iterate over every frame in the gif
    for frame_index in range(0, gif.n_frames):
        gif.seek(frame_index)

        # must copy the frame out of the gif, since thumbnail() modifies the image in-place
        frame = gif.copy()
        frame.thumbnail((matrix.width, matrix.height), Image.BICUBIC)

        newFrame = ImageUtils.duplicateScreen(
            ImageUtils.limitCurrent(
                frame.convert("RGB"), MatrixConstants.PANEL_COUNT
            )
        )

        canvas = matrix.CreateFrameCanvas()
        canvas.SetImage(newFrame)
        canvases.append(canvas)
    
    # Note: technically in a gif, different frames can have different durations, 
    # but I'm too lazy to change this.
    return (canvases, gif.info['duration'])


class GifMode(LEDmode):
    
    def __init__(self, matrix: RGBMatrix, gifPath: str):
        self.matrix = matrix
        animation = Image.open(gifPath)

        try:
            self.num_frames = animation.n_frames
        except Exception:
            sys.exit("provided image is not a gif")

        self.gifCanvases = compileGif(animation, matrix)
        animation.close()

    def startup(self):
        self.cur_frame = 0
        self.start_time = time.time()

        self.matrix.SwapOnVSync(self.gifCanvases[0][0])

    def periodic(self):
        # display each frame one after the other
        if ((time.time()) - self.start_time) > (self.gifCanvases[1] / 1000):
            self.start_time = time.time() # reset timer
            self.cur_frame = (self.cur_frame + 1) % self.num_frames # increment frame counter
            self.matrix.SwapOnVSync(self.gifCanvases[0][self.cur_frame]) # go to next frame

    def onEnd(self):
        pass