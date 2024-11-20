
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys
# from LEDModes.idleMode import IdleMode
from LEDModes.GifMode import GifMode
from constants import MatrixConstants
from constants import ImageConstants
from constants import GifConstants
from utils import ImageUtils
from PIL import Image

"""
This file is for testing LED states without having to hook up the raspberry pi to the robot.
"""

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = MatrixConstants.HEIGHT
    options.cols = MatrixConstants.WIDTH
    options.gpio_slowdown = 4
    options.chain_length = MatrixConstants.PANEL_COUNT
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

    matrix = RGBMatrix(options = options)

    with Image.open(ImageConstants.LOADING) as loadingImage:
        matrix.SetImage(ImageUtils.duplicateScreen(loadingImage))

    LED_MODE = GifMode(matrix, GifConstants.IDLE)

    try:
        print("Press CTRL-C to stop.")
        LED_MODE.startup()

        while True:
            LED_MODE.periodic()

    except KeyboardInterrupt: # for debugging purposes
        LED_MODE.onEnd()
        sys.exit(0)
