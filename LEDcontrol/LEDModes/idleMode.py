import time
import sys
from constants import GifConstants

# from LEDcontrol.simulation.rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import RGBMatrix # type: ignore

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


def compileGif(gif: Image.Image, matrix: RGBMatrix) -> list:
    """
    Takes a gif and turns it into a list of canvases that can be 
    displayed one after the other. Also returns the duration of the gif.
    """

    canvases = []

    # iterate over every frame in the gif
    for frame_index in range(0, gif.n_frames):
        gif.seek(frame_index)

        # must copy the frame out of the gif, since thumbnail() modifies the image in-place
        frame = gif.copy()
        frame.thumbnail((matrix.width, matrix.height), Image.BICUBIC)

        canvas = matrix.CreateFrameCanvas()
        canvas.SetImage(frame.convert("RGB"))
        canvases.append(canvas)
    
     # Note: technically in a gif, different frames can have different durations, 
     # but I'm too lazy to change this.
    return (canvases, gif.info['duration'])


class IdleMode(LEDmode):
    
    def __init__(self, matrix, playStartup=False):
        self.matrix = matrix
        self.playStartup = playStartup

        self.gifCanvases = compileGif(StartupANI, matrix)

    def startup(self):
        self.cur_frame = 0

    def periodic(self):
        # display each frame one after the other
        num_frames = Startup_num_frames
        self.matrix.SwapOnVSync(self.gifCanvases[0][self.cur_frame])
        self.cur_frame = (self.cur_frame + 1) % num_frames
        time.sleep(self.gifCanvases[1] / 1000)  

    def onEnd(self):
        pass