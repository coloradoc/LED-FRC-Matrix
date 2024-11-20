#!/usr/bin/env python
import math
from rgbmatrix import RGBMatrix
from PIL import Image, ImageFilter
from constants import ImageConstants as IC

from LEDModes.LEDmode import LEDmode

rightEye = Image.open(IC.PROOT_PATH + "rightEye.png")
leftEye = Image.open(IC.PROOT_PATH + "leftEye.png")
rightSmile = Image.open(IC.PROOT_PATH + "rightSmile.png")
leftSmile = Image.open(IC.PROOT_PATH + "leftSmile.png")
nose = Image.open(IC.PROOT_PATH + "nose.png")
faceSmall = Image.open(IC.PROOT_PATH + "faceSmall.png")
faceNormal = Image.open(IC.PROOT_PATH + "faceNormal.png")
googleLeft = Image.open(IC.PROOT_PATH + "googleLeft.png")
googleRight = Image.open(IC.PROOT_PATH + "googleRight.png")
blinklyLeft = Image.open(IC.PROOT_PATH + "blinklyLeft.png")
blinklyRight = Image.open(IC.PROOT_PATH + "blinklyRight.png")

class prootMode(LEDmode):

    def __init__(self, matrix: RGBMatrix):
        self.matrix = matrix


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
        x = prootMode.sigma(math.sin(x))*math.sqrt(abs(math.sin(x)))
        return x
    

    def setImg(self, parts):
        # Background
        composite_image = Image.new("RGBA", (self.matrix.width, self.matrix.height))
        for part in parts:
            part[0].thumbnail((self.matrix.width, self.matrix.height), Image.BICUBIC)
            img = prootMode.rotato(part[0], part[1], part[2], part[3], part[4])
            composite_image.alpha_composite(img)

        self.matrix.SetImage(composite_image.convert('RGB'))


    def startup(self):
        
        self.angle = 0
        self.angleWarp = 0
        self.directionFlip = False
        self.x = 0
        self.y = 0
    
        self.rightEyeBox = prootMode.getImageCenter(rightEye)
        self.leftEyeBox = prootMode.getImageCenter(leftEye)
        self.googleLeftBox = prootMode.getImageCenter(googleLeft)
        self.googleRightBox = prootMode.getImageCenter(googleRight)
        self.noseBox = prootMode.getImageCenter(nose)
        self.rightSmileBox = prootMode.getImageCenter(rightSmile)
        self.leftSmileBox = prootMode.getImageCenter(leftSmile)


    def periodic(self):
        if not self.directionFlip:
            self.angleWarp += .0025
        else:
            self.angleWarp -= .0025
        if self.angleWarp >= 2:
            self.directionFlip = True
        if self.angleWarp <= 0:
            self.directionFlip = False
        self.angle += .5
        self.x += 0
        self.y += 0
        
        self.setImg([ 
                #[googleLeft, googleLeftBox, angleWarp*20, math.sin(x)*2, steepSin(y)*2], 
                #[googleRight, googleRightBox, -angleWarp*20, math.sin(x)*2, steepSin(y)*2], 
                [leftEye, self.leftEyeBox, -self.angleWarp*2, math.sin(self.x)*2, prootMode.steepSin(self.y)*2], 
                [rightEye, self.rightEyeBox, self.angleWarp*2, math.sin(self.x)*2, prootMode.steepSin(self.y)*2], 
                [nose, self.noseBox, 0, 0, 0], 
                [rightSmile, self.rightSmileBox, self.angleWarp, 0, 0], 
                [leftSmile, self.leftSmileBox, -self.angleWarp, 0,0]
            ])
    

    def onEnd(self):
        pass
    