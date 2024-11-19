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
gifList = []
gif_folder = "/home/pi/LEDcontrol/media/gif"
for gif_file in glob.glob(os.path.join(gif_folder, "*.gif")):
    gif = Image.open(gif_file)
    gifList.append(gif)



# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.gpio_slowdown = 4
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
matrix = RGBMatrix(options = options)

#cut gif into frames to be loaded into the canvases list
def loadGif(gif):
    try:
        num_frames = gif.n_frames
    except Exception:
        sys.exit("provided image is not a gif")

    # Preprocess the gifs frames into canvases to improve playback performance
    canvases = []
    print("Preprocessing gif, this may take a moment depending on the size of the gif...")
    for frame_index in range(0, num_frames):
        gif.seek(frame_index)
        # must copy the frame out of the gif, since thumbnail() modifies the image in-place
        frame = gif.copy()
        frame.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        canvas = matrix.CreateFrameCanvas()
        canvas.SetImage(frame.convert("RGB"))
        canvases.append(canvas)
    # Close the gif file to save memory now that we have copied out all of the frames
    gif.close()

    print("Completed Preprocessing, displaying gif")
    return [canvases, num_frames]


#run gif spliting function to load frames into canvases list
canvasesList= []

for gif in gifList:
    canvasesList.append(loadGif(gif))

def playGif(canvas):
    # Infinitely loop through the gif
    cur_frame = 0
    num_frames = canvas[1]
    while num_frames != cur_frame + 1:
        matrix.SwapOnVSync(canvas[0][cur_frame])
        cur_frame = (cur_frame + 1) % num_frames
        time.sleep(.03)  # Adjust this value to make the gif run faster or slower

try:
    print("Press CTRL-C to stop.")
    while True:
        for canvas in canvasesList:
            playGif(canvas)

except KeyboardInterrupt:
    sys.exit(0)