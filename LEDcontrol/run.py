import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions

from networktables import NetworkTables

from PIL import Image

from LEDModes import *
from LEDModes.IdleMode import IdleMode
from LEDModes.GifMode import GifMode
from constants import NetworkTablesConstants as NTConstants, GifConstants, ImageConstants, MatrixConstants
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

    # Initialize networktables
    NetworkTables.initialize(server=NTConstants.ROBOT_IP)

    LEDDataTable = NetworkTables.getTable(NTConstants.LED_DATA_TABLE)
    indexTab = NetworkTables.getTable(NTConstants.INDEX_TAB_NAME)
    shooterTab = NetworkTables.getTable(NTConstants.SHOOTER_TAB_NAME)

    LED_MODES = [IdleMode(matrix), GifMode(matrix, GifConstants.FeedMe), GifMode(matrix, GifConstants.BoyKisser), GifMode(matrix, GifConstants.Yipee), GifMode(matrix, GifConstants.Yummy)]

    led_index = 0
    led_mode = LED_MODES[led_index]

    connectionEstablished = False

    def connectionListener(isConnected, info):
        global connectionEstablished

        if isConnected:
            connectionEstablished = True
            print("Connected to robot")
        else:
            connectionEstablished = False
            print("Disconnected from robot")

    # Detects when we connect/disconnect from robot.
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    def ballDetectedListener(source, key, value, inNew):
        global led_index

        if value == True:
            led_index = 4
        
    indexTab.addEntryListener(ballDetectedListener, key=NTConstants.IS_BALL_DETECTED_KEY)

    # use try statement so the code can be ended via keypress
    # for testing purposes
    try:
        print("Press CTRL-C to stop.")
        
        led_mode.startup()

        # Main program loop
        while True:
            # Get LED mode from networktables
            led_index = int(LEDDataTable.getNumber(NTConstants.LED_INDEX_KEY, led_index))
            
            # Safety: don't attempt to use an index that doesn't exist
            if led_index + 1 > len(LED_MODES):
                led_index = 0

            # Switch LED modes if necessary
            if led_index != LED_MODES.index(led_mode):
                led_mode.onEnd()
                led_mode = LED_MODES[led_index]
                led_mode.startup()

            # Run periodic and switch modes if current mode has ended
            if led_mode.periodic():
                led_index = 0
                LEDDataTable.putNumber(NTConstants.LED_INDEX_KEY, led_index)

    except KeyboardInterrupt: # For debugging purposes
        led_mode.onEnd()
        sys.exit(0)