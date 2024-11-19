#!/usr/bin/env python
from samplebase import SampleBase
from LEDcontrol.rgbmatrixsim import graphics #type: ignore
import time

font = graphics.Font()
font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf")

class textFlash(SampleBase):
    def __init__(self, text="Launch", scroll_speed=0.05, r=255, g=255, b=255, backgroundColor="red", timeToRun=5, *args, **kwargs):
        super(textFlash, self).__init__(*args, **kwargs)
        self.text = text
        self.scroll_speed = scroll_speed
        self.r = r
        self.g = g
        self.b = b
        self.backgroundColor = backgroundColor
        self.timeToRun = timeToRun

    def run(self):
        scroll_speed = self.scroll_speed
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        my_text = self.text
        my_r = self.r
        my_g = self.g
        my_b = self.b
        my_background_color = self.backgroundColor
        my_time_to_run = self.timeToRun

        startTime = time.time()
        endTime = time.time()+my_time_to_run

        continuum = 0
        direction = 1  # Direction of continuum change (1 for increasing, -1 for decreasing)
        increment = 5  # Increment size for continuum change

        textColor = graphics.Color(my_r, my_g, my_b)
        pos = self.offscreen_canvas.width

        while endTime > time.time():
            self.usleep(1000)  # Adjust the sleep time for smoother transition
            continuum += direction * increment
            if continuum >= 255:
                continuum = 255
                direction = -1
            elif continuum <= 0:
                continuum = 0
                direction = 1

            if my_background_color == 'red':
                red = continuum
                green = 0
                blue = 0
            if my_background_color == 'green':
                red = 0
                green = continuum
                blue = 0
            if my_background_color == 'blue':
                red = 0
                green = 0
                blue = continuum

            # Fill the background with pulsing color
            self.offscreen_canvas.Fill(red, green, blue)

            # Draw scrolling text
            len = graphics.DrawText(self.offscreen_canvas, font, pos, 20, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = self.offscreen_canvas.width

            # Swap buffers to display
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

            # Sleep for smooth scrolling effect
            time.sleep(scroll_speed)
