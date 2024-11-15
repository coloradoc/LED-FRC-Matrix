from PIL import Image
import pygame
from pygame.locals import *


class RGBMatrixOptions:

    def __init__(self):
        pass


class Canvas:

    def __init__(self):
        pass
    
    def SetImage(self, img: Image.Image):
        self.image = img


# Increase window size to make it easier to see on a desktop.
DISPLAY_SCALE = 7


class RGBMatrix:

    """
        Represents an RGB Matrix display or multiple Matrices lined up horizontally.
    """
    def __init__(self, options: RGBMatrixOptions = None):
        self._options = options

        self.width: int = options.cols * options.chain_length
        self.height: int = options.rows

        # Initialize Pygame
        pygame.init()

        # Set up the Pygame window
        self.screen = pygame.display.set_mode((self.width*DISPLAY_SCALE, self.height*DISPLAY_SCALE))
        pygame.display.set_caption("Image Stream")
    

    # Destructor
    def __del__(self):
        pygame.quit()
       
    
    # Displays an image on the Matrix.
    # img: the image to display
    def SetImage(self, img: Image.Image):
        # Images larger than the screen are cut off
        formatted_img = img.crop((0, 0, self.width, self.height))

        # Increase size for easier viewing
        formatted_img = formatted_img.resize((self.width*DISPLAY_SCALE, self.height*DISPLAY_SCALE), Image.Resampling.BOX)

        # Format into pygame image
        Pygame_image = pygame.image.fromstring(formatted_img.tobytes(), formatted_img.size, formatted_img.mode)

        self.screen.fill((0, 0, 0))  # Clear screen
        self.screen.blit(Pygame_image, (0, 0))  # Draw image
        pygame.display.flip()  # Update display

        # While we're at it let's also check for events
        # This should really be done periodically but there's no thread-safe way to do it
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


    def CreateFrameCanvas(self) -> Canvas:
        return Canvas()
    

    def SwapOnVSync(self, canvas: Canvas):
        self.SetImage(canvas.image)
