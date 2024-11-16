import sys
import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions

from networktables import NetworkTables

from PIL import Image

from LEDModes import *
from LEDModes.IdleMode import IdleMode
from LEDModes.prootMode import prootMode
from LEDModes.GifMode import GifMode
from constants import NetworkTableConstants, GifConstants, ImageConstants, MatrixConstants
from utils import ImageUtils

"""
This is the main file to be ran on the raspberry pi.
Connects to networktables and manages the LED state.
"""

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = MatrixConstants.HEIGHT
    options.cols = MatrixConstants.WIDTH
    options.brightness = MatrixConstants.BRIGHTNESS
    options.gpio_slowdown = 4
    options.chain_length = MatrixConstants.PANEL_COUNT
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

    matrix = RGBMatrix(options = options)

    # Do loading screen while gifs are processed
    with Image.open(ImageConstants.LOADING) as loadingImage:
        matrix.SetImage(ImageUtils.duplicateScreen(loadingImage))

    sd = NetworkTables.getTable("/SmartDashboard") # this may need to be moved lower to avoid errors
    indexTab = sd.getSubTable(NetworkTableConstants.INDEX_TAB_NAME)
    shooterTab = sd.getSubTable(NetworkTableConstants.SHOOTER_TAB_NAME)

    LED_MODES = [IdleMode(matrix), GifMode(matrix, GifConstants.FeedMe), GifMode(matrix, GifConstants.BoyKisser), GifMode(matrix, GifConstants.Yipee)]

    led_index = 0
    led_mode = LED_MODES[led_index]

    connectionEstablished = False

    def connectionListener():
        global connectionEstablished
        connectionEstablished = True

    def dpadListener(key: str, value: int, isNew: int):
        led_index = value

    def ballDetectionListener(key: str, value: bool, isNew: int):
        if value:
            led_index = 4

    sd.addEntryListener(dpadListener, key=NetworkTableConstants.DPAD_INDEX_KEY)
    indexTab.addEntryListener(ballDetectionListener, key=NetworkTableConstants.IS_BALL_DETECTED_KEY)

    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    # # wait until connected to robot
    # while not connectionEstablished:
    #     time.sleep(0.05)
    
    # use try statement so the code can be ended via keypress
    # for testing purposes
    try:
        print("Press CTRL-C to stop.")
        
        led_mode.startup()

        # Main program loop
        while True:
            if led_index != LED_MODES.index(led_mode):
                led_mode.onEnd()
                led_mode = LED_MODES[led_index]
                led_mode.startup()

            if led_mode.periodic():
                led_index = 0

    except KeyboardInterrupt: # For debugging purposes
        led_mode.onEnd()
        sys.exit(0)
        
