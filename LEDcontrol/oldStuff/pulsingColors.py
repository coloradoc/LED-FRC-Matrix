#!/usr/bin/env python
from samplebase import SampleBase


class PulsingColors(SampleBase):
    def __init__(self, *args, **kwargs):
        super(PulsingColors, self).__init__(*args, **kwargs)

    def run(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        continuum = 0
        direction = 1  # Direction of continuum change (1 for increasing, -1 for decreasing)
        increment = 5  # Increment size for continuum change

        while True:
            self.usleep(5000)  # Adjust the sleep time for smoother transition
            continuum += direction * increment
            if continuum >= 255:
                continuum = 255
                direction = -1
            elif continuum <= 0:
                continuum = 0
                direction = 1

            red = continuum
            green = 0
            blue = 0

            self.offscreen_canvas.Fill(red, green, blue)
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

