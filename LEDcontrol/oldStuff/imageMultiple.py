#!/usr/bin/env python
import time
import sys
import os 
import glob
from LEDcontrol.rgbmatrixsim import RGBMatrix, RGBMatrixOptions #type: ignore
from PIL import Image

#setup gifs to load 

#gif = Image.open("media\gif\vap.gif")
#gif2 = Image.open("media\gif\4D.gif")
patterns = ["*.gif", "*.png", "*.jpg", "*.PNG", "*.JPG"]

gifList = []
gif_folder = "/home/pi/LEDcontrol/media/sponsorLogos"
for pattern in patterns:
    for gif_file in glob.glob(os.path.join(gif_folder, pattern)):
        print(gif_file)
        gif = Image.open(gif_file)
        gifList.append(gif)


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.gpio_slowdown = 4
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
matrix = RGBMatrix(options = options)

def clearScreen():
    black_image = Image.new("RGB", (matrix.width, matrix.height), (0, 0, 0))
    matrix.SetImage(black_image)

# Make image fit our screen.
def setImg(imageSet):
    imageSet.thumbnail((64, 32), Image.ANTIALIAS)

    matrix.SetImage(imageSet.convert('RGB'))

    print(matrix.width)
    print(matrix.height)


try:
    print("Press CTRL-C to stop.")
    while True:
        for img in gifList:
            setImg(img)
            time.sleep(2)
            clearScreen()
except KeyboardInterrupt:
    sys.exit(0)

