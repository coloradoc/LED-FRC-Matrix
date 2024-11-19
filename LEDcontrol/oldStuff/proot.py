#!/usr/bin/env python
import time
import sys
import math
from LEDcontrol.rgbmatrixsim import RGBMatrix, RGBMatrixOptions #type: ignore
from PIL import Image, ImageFilter


rightEye = Image.open("/home/pi/LEDcontrol/media/prootImg/rightEye.png")
leftEye = Image.open("/home/pi/LEDcontrol/media/prootImg/leftEye.png")
rightSmile = Image.open("/home/pi/LEDcontrol/media/prootImg/rightSmile.png")
leftSmile = Image.open("/home/pi/LEDcontrol/media/prootImg/leftSmile.png")
nose = Image.open("/home/pi/LEDcontrol/media/prootImg/nose.png")
faceSmall = Image.open("/home/pi/LEDcontrol/media/prootImg/faceSmall.png")
faceNormal = Image.open("/home/pi/LEDcontrol/media/prootImg/faceNormal.png")
googleLeft = Image.open("/home/pi/LEDcontrol/media/prootImg/googleLeft.png")
googleRight = Image.open("/home/pi/LEDcontrol/media/prootImg/googleRight.png")
blinklyLeft = Image.open("/home/pi/LEDcontrol/media/prootImg/blinklyLeft.png")
blinklyRight = Image.open("/home/pi/LEDcontrol/media/prootImg/blinklyRight.png")


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.gpio_slowdown = 4
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Takes an RGBA image and returns the viewbox of the non-transparent part of the image
def getImageCenter(img: Image):
    minX = -1
    maxX = 0
    minY = -1
    maxY = 0
    for x in range(0, img.width):
        for y in range(0, img.height):
            if img.getpixel((x, y))[3] != 0:
                if minX == -1:
                    minX = x
                maxX = max(maxX, x)
                if minY == -1:
                    minY = y
                else: 
                    minY = min(minY, y)
                maxY = max(maxY, y)
    return (minX, minY, maxX, maxY)


def rotatoLarge(img, regionBox, angle, y, x):
    # Crop the region from the original image
    list = []
    for i in regionBox:
        list.append(i)

    list[3] = list[3]+50

    regionBox = list

    croppedRegion = img.crop(regionBox)
    
    # Rotate the cropped region
    rotatedRegion = croppedRegion.rotate(angle, resample=Image.BICUBIC)
    
    # Create a new blank image with the same size as the original image
    blankImage = Image.new('RGBA', img.size, (0, 0, 0, 0))
    
    # Calculate the new position, allowing for fractional movement
    newPosition = (regionBox[0] + int(y), regionBox[1] + int(x))
    
    # Paste rotated region with antialiasing
    blankImage.paste(rotatedRegion, newPosition, rotatedRegion.filter(ImageFilter.SMOOTH))
    
    return blankImage

def rotato(img, regionBox, angle, y, x): 

    croppedRegion = img.crop(regionBox)
    croppedRegion.thumbnail(croppedRegion.size, Image.Resampling.LANCZOS)
    rotatedRegion = croppedRegion.rotate(angle, resample=Image.BICUBIC)
    newPostion = (regionBox[0] + int(y), regionBox[1] + int(x))

    blankImage = Image.new('RGBA', img.size)
    blankImage.getpixel((0, 0))
    blankImage.paste(rotatedRegion, newPostion, rotatedRegion)


    return blankImage

def sigma(x):
    return abs(x)==x

def steepSin(x):
    x = sigma(math.sin(x))*math.sqrt(abs(math.sin(x)))
    return x
def setImg(parts):
    # Background
    composite_image = Image.new("RGBA", (matrix.width, matrix.height))
    for part in parts:
        part[0].thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        img = rotato(part[0], part[1], part[2], part[3], part[4])
        composite_image.alpha_composite(img)

    matrix.SetImage(composite_image.convert('RGB'))

    #print(matrix.width)
    #print(matrix.height)
try:
    print("Press CTRL-C to stop.")
    angle = 0
    angleWarp = 0
    directionFlip = False
    x = 0
    y = 0
    print(getImageCenter(googleLeft))
    rightEyeBox = getImageCenter(rightEye)
    leftEyeBox = getImageCenter(leftEye)
    googleLeftBox = getImageCenter(googleLeft)
    googleRightBox = getImageCenter(googleRight)
    noseBox = getImageCenter(nose)
    rightSmileBox = getImageCenter(rightSmile)
    leftSmileBox = getImageCenter(leftSmile)
    while True:
        if not directionFlip:
            angleWarp += .01
        else:
            angleWarp -= .01
        if angleWarp >= 2:
            directionFlip = True
        if angleWarp <= 0:
            directionFlip = False
        angle += .5
        x += 0
        y += 0
        
        setImg([ # (24, 0, 44, 18)
                #[googleLeft, googleLeftBox, angleWarp*20, math.sin(x)*2, steepSin(y)*2], 
                #[googleRight, googleRightBox, -angleWarp*20, math.sin(x)*2, steepSin(y)*2], 
                [leftEye, leftEyeBox, -angleWarp*2, math.sin(x)*2, steepSin(y)*2], 
                [rightEye, rightEyeBox, angleWarp*2, math.sin(x)*2, steepSin(y)*2], 
                [nose, noseBox, 0, 0, 0], 
                [rightSmile, rightSmileBox, angleWarp, 0, 0], 
                [leftSmile, leftSmileBox, -angleWarp, 0,0]
            ])
except KeyboardInterrupt:
    sys.exit(0)