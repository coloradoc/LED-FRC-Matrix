from PIL import Image, ImageOps
from constants import MatrixConstants

class ImageUtils:


    def blendToRGB(img: Image.Image, background_color: tuple = (0, 0, 0)) -> Image.Image:
        """
        Converts a RGBA image to RGB by blending partially transparent pixels with a black
        background (as opposed to displaying partially transparent pixels as opaque).
        """

        # Create a background image with the same size
        background = Image.new('RGB', img.size, background_color)

        # Composite RGBA image over black background
        return Image.alpha_composite(background.convert('RGBA'), img.convert("RGBA")).convert('RGB')
    

    def limitCurrent(img: Image.Image, numberOfPanels: int) -> Image.Image:
        """
        Attempts to reduce the amount of current used by the panels by estimating the 
        current needed to display an image and dimming the entire image if necessary.
        The image passed in should be an RGB image with no transparency.
        """
        
        # Using image data is faster than modifying the image itself
        image_data = list(img.getdata())

        def getImageBrightness(img):
            """
            Estimate the brightness of an image by added the red, green, and blue channel 
            of every pixel.
            """

            brightnessLevel = 0

            for pixel in image_data:
                brightnessLevel += pixel[0] + pixel[1] + pixel[2]
            
            return brightnessLevel
        
        def brightnessReduction(imgData, amount):

            """Reduces the brightness of every pixel by a specified amount."""

            for pixelIndex in range(0, len(imgData)):
                newColor = [0, 0, 0] # this will contain the dimmed channels
                currentPixel = imgData[pixelIndex] # current color for this pixel

                for i in range(0, 3):
                    if currentPixel[i] - amount >= 0:
                        newColor[i] = currentPixel[i] - amount

                imgData[pixelIndex] = tuple(newColor)

        # The amperage of one panel at full brightness
        FOUR_AMPS = 255 * 3 * 32 * 64
        # One amp ~= 391,680

        # The brightness decrease if every pixel is brought down by 1
        ONE_REDUCTION = 3 * 32 * 64
        
        deadPixels = 0

        # Get the number of channels at 0
        for pixel in image_data:
            for channel in pixel:
                deadPixels += 1 if channel == 0 else 0
        # print("dead pixels: " + str(deadPixels))

        # newImage = image_data.copy()
        
        # Repeat the dimming process until the screens are dim enough
        while (brightness := getImageBrightness(image_data) * numberOfPanels) > FOUR_AMPS / 2.1:

            # print("Reducing brightness: " + str(brightness))

            reductionAmmount = (brightness - int(FOUR_AMPS / 2.1)) // ((ONE_REDUCTION - deadPixels) * numberOfPanels)

            if reductionAmmount == 0:
                reductionAmmount = 1

            brightnessReduction(image_data, reductionAmmount)
        
        # return an image that uses the new dimmed values
        new_image = Image.new(img.mode, img.size)
        new_image.putdata(image_data)

        return new_image
    

    def duplicateScreen(img: Image.Image) -> Image.Image:
        """
        Takes an image for one screen and duplicates it horizontally so
        that it will appear on both screens.
        """
        newImage = Image.new("RGB", (MatrixConstants.WIDTH*2, MatrixConstants.HEIGHT))

        newImage.paste(img, (0, 0))
        newImage.paste(img, (MatrixConstants.WIDTH, 0))

        return newImage
    

    def mirrorScreen(img: Image.Image, invertMirroring = False) -> Image.Image:
        """
        Takes an image for one screen and mirrors it horizontally so
        that it will appear on both screens facing the same direction.
        """
        newImage = Image.new("RGB", (MatrixConstants.WIDTH*2, MatrixConstants.HEIGHT))
        
        if invertMirroring:
            newImage.paste(ImageOps.mirror(img), (0, 0))
            newImage.paste(img, (MatrixConstants.WIDTH, 0))
        else:
            newImage.paste(img, (0, 0))
            newImage.paste(ImageOps.mirror(img), (MatrixConstants.WIDTH, 0))

        return newImage
    
    def compileGif(gif: Image.Image, matrix) -> list:
        """
        Takes a gif and returns a tuple containing a list of canvases that can be 
        displayed one after the other, along with the duration of the gif.
        """

        canvases = []
        durations = []
        
        # iterate over every frame in the gif
        for frame_index in range(0, gif.n_frames):
            gif.seek(frame_index)

            # must copy the frame out of the gif, since thumbnail() modifies the image in-place
            frame = gif.copy()
            frame.thumbnail((matrix.width, matrix.height), Image.BICUBIC)

            durations.append(frame.info["duration"])

            newFrame = ImageUtils.duplicateScreen(
                ImageUtils.limitCurrent(
                    frame.convert("RGB"), MatrixConstants.PANEL_COUNT
                )
            )

            canvas = matrix.CreateFrameCanvas()
            canvas.SetImage(newFrame)
            canvases.append(canvas)
        
        return (canvases, durations)
            