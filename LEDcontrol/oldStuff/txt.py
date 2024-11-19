#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from LEDcontrol.rgbmatrixsim import graphics #type: ignore
import time

font = graphics.Font()
font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf")

class RunText(SampleBase):
    """
    Display scrolling text on an RGB LED panel.

    Parameters:
        text (str): The text to display on the RGB LED panel.
        scroll speed (float): The scroll speed of the text
    """
    def __init__(self, text="Launch", scroll_speed=0.05, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.text = text
        self.scroll_speed = scroll_speed

    def run(self):
        my_scroll_speed = self.scroll_speed
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        textColor = graphics.Color(255, 0, 0)
        pos = offscreen_canvas.width
        my_text = self.text

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(my_scroll_speed)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


